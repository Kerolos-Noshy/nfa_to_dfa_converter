from .nfa import NFA
from .dfa import DFA
from .state_type import StateType
from .state import State
from .transition import Transition

class AutomataConverter:
    def __init__(self, nfa: NFA, minimized):
        self.nfa = nfa
        self.transition_table = []
        self.handled_states = set()
        self.unhandled_states = set()
        self.phi_state_exist = False
        self.minimized = minimized
        self.PHI = "?";

    def convert_to_dfa_table(self):
        if self.nfa.has_epsilon():
            self.nfa = self.convert_to_nfa(self.nfa)
        
        self.add_table_row(self.nfa.get_initial_state())
        self.process_unhandled_states()

        if self.phi_state_exist:
            self.add_phi_row()
        return self.transition_table

    def convert_to_dfa(self, minimized):
        self.handled_states.clear()
        dfa = DFA()
        dfa.set_alphabets(self.nfa.get_alphabets())

        phi = State(self.PHI)
        if self.nfa.has_epsilon:
            self.nfa = self.convert_to_nfa(self.nfa)
        
        start_state = self.nfa.get_initial_state()
        new_state = State(start_state.get_name())
        dfa.add_state(new_state)
        dfa.set_initial_state(new_state)

        if start_state in self.nfa.get_final_states():
            dfa.add_final_state(new_state)

        self.handled_states.add(start_state)

        for alphabet in self.nfa.get_alphabets():
            next_states = self.get_next_states_for_alphabet(start_state, alphabet)
            if next_states:
                if len(next_states) == 1:
                    new_state_transition = next_states[0]
                    if not self.is_state_exist(self.handled_states, new_state_transition):
                        self.unhandled_states.add(new_state_transition)
                    new_state.add_transition(Transition(alphabet, next_states[0]))
                else:
                    combined_state = self.create_combined_state(next_states)
                    new_state.add_transition(Transition(alphabet, combined_state))
            else:
                self.phi_state_exist = True
                new_state.add_transition(Transition(alphabet, phi))

        while self.unhandled_states:
            state = self.unhandled_states.pop()
            if state:
                new_state = State(state.get_name())

            for alphabet in self.nfa.get_alphabets():
                next_states = self.get_next_states_for_alphabet(state, alphabet)
                if next_states:
                    if len(next_states) == 1:
                        new_state.add_transition(Transition(alphabet, next_states[0]))
                        if not self.is_state_exist(self.handled_states, next_states[0]):
                            self.unhandled_states.add(next_states[0])
                    else:
                        combined_state = self.create_combined_state(next_states)
                        new_state.add_transition(Transition(alphabet, combined_state))
                else:
                    self.phi_state_exist = True
                    new_state.add_transition(Transition(alphabet, phi))

            self.handled_states.add(state)
            dfa.add_state(new_state)

            if state in self.nfa.get_final_states():
                final_states = [state.get_name() for state in dfa.get_final_states()]
                if state.get_name() not in final_states:
                    dfa.add_final_state(new_state)

        if self.phi_state_exist:
            dfa.add_state(phi)
            for alpha in self.nfa.get_alphabets():
                dfa.add_transition(phi, alpha, phi)

        return dfa

    def add_table_row(self, state):
        row = [state]
        self.handled_states.add(state)

        for symbol in self.nfa.get_alphabets():
            next_states = self.get_next_states_for_alphabet(state, symbol)
            if next_states:
                if len(next_states) == 1:
                    new_state = next_states[0]
                    if not self.is_state_exist(self.handled_states, new_state):
                        self.unhandled_states.add(new_state)
                    row.append(new_state)
                else:
                    combined_state = self.create_combined_state(next_states)
                    row.append(combined_state)
            else:
                phi = State(self.PHI)
                self.phi_state_exist = True
                row.append(phi)

        self.transition_table.append(row)

    def get_next_states_for_alphabet(self, state, alphabet):
        if state:
            return [t.get_next_state() for t in state.get_transitions() if t.get_alphabet() == alphabet]
        

    def create_combined_state(self, next_states):
        sorted_names = sorted([s.get_name() for s in next_states])
        new_state_name = "".join(sorted_names)
        state_type = None

        for next_state in next_states:
            if self.nfa.get_state_type(next_state) == StateType.FINAL:
                state_type = StateType.FINAL

        # Check if the new composed state is already handled or unhandled
        for s in self.handled_states:
            if s.get_name() == new_state_name:
                return s
        for s in self.unhandled_states:
            if s.get_name() == new_state_name:
                return s

        new_state = State(new_state_name)
        if state_type == StateType.FINAL:
            self.nfa.add_final_state(new_state)

        for next_state in next_states:
            for t in next_state.get_transitions():
                new_state.add_transition(t)

        self.unhandled_states.add(new_state)
        return new_state

    def convert_to_nfa(self, epsilon_nfa):
        converted_nfa = NFA()
        initial_state = State(epsilon_nfa.get_initial_state().get_name())
        converted_nfa.add_state(initial_state)
        converted_nfa.set_initial_state(initial_state)

        for curr in epsilon_nfa.get_states():
            current_state = converted_nfa.get_state_by_name(curr.get_name())
            for symbol in epsilon_nfa.get_alphabets():
                epsilon_closure = set()
                next_states = []

                for state in self.get_epsilon_closure(curr):
                    next_states.extend(self.get_next_states_for_alphabet(state, symbol))

                for s in next_states:
                    epsilon_closure.update(self.get_epsilon_closure(s))

                for s in epsilon_closure:
                    new_state = converted_nfa.get_state_by_name(s.get_name())
                    if current_state:
                        converted_nfa.add_transition(current_state, symbol, new_state)
                        if epsilon_nfa.get_state_type(s) == StateType.FINAL:
                            converted_nfa.add_final_state(new_state)

        return converted_nfa

    def get_epsilon_closure(self, state):
        epsilon_closure = set()
        visited = set()
        stack = [state]

        while stack:
            current_state = stack.pop()
            if current_state not in visited:
                visited.add(current_state)
                epsilon_closure.add(current_state)

                for t in current_state.get_transitions():
                    if t.get_alphabet() == 'ε':
                        stack.append(t.get_next_state())

        return epsilon_closure

    def process_unhandled_states(self):
        while self.unhandled_states:
            state = self.unhandled_states.pop()
            self.add_table_row(state)

    def is_state_exist(self, states, state):
        if isinstance(state, State):
            return any(s.get_name() == state.get_name() for s in states)
        return False

    def add_phi_row(self):
        phi = State(self.PHI)
        row = [phi] * (len(self.nfa.get_alphabets()) + 1)
        self.transition_table.append(row)
