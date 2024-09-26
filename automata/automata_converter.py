from collections import deque
from .state import State
from .state_type import StateType
from .transition import Transition
from .nfa import NFA
from .dfa import DFA


class AutomataConverter:
    def __init__(self, nfa):
        self.nfa = nfa
        self.transition_table = []
        self.handled_states = set()
        self.unhandled_states = set()
        self.phi_state_exist = False
        self.PHI = 'Ø'

    # def convert_to_dfa(self):
    #     if self.nfa.has_epsilon():
    #         self.nfa = self.convert_to_nfa(self.nfa)
    #     self.add_table_row(self.nfa.get_initial_state())
    #     self.process_unhandled_states()
    #
    #     if self.phi_state_exist:
    #         self.add_phi_row()
    #
    #     return self.transition_table

    def convert_to_dfa(self):
        self.handled_states.clear()
        dfa = DFA()
        dfa.set_alphabets(self.nfa.get_alphabets())
        if (dfa.get_alphabets().__contains__('e')):
            dfa.alphabets.remove('e')

        phi = State(self.PHI)
        if self.nfa.has_epsilon:
            self.nfa = self.convert_to_nfa(self.nfa)

        start_state = self.nfa.get_initial_state()
        new_state = State(start_state.name)
        dfa.add_state(new_state)
        dfa.set_initial_state(new_state)

        if start_state in self.nfa.get_final_states():
            dfa.add_final_state(new_state)

        self.handled_states.add(start_state)

        for alphabet in self.nfa.get_alphabets():
            next_states = self.get_next_states_for_alphabet(start_state, alphabet)
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

        while self.unhandled_states:
            state = self.unhandled_states.pop()
            new_state = State(state.name)

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
                dfa.add_final_state(new_state)

        if self.phi_state_exist:
            dfa.add_state(phi)
            for alphabet in self.nfa.get_alphabets():
                dfa.add_transition(phi, alphabet, phi)

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
                    new_state = self.create_combined_state(next_states)
                    row.append(new_state)
            else:
                phi = State(self.PHI)
                self.phi_state_exist = True
                row.append(phi)

        self.transition_table.append(row)

    def get_next_states_for_alphabet(self, state, alphabet):
        return [transition.get_next_state() for transition in state.get_transitions() if transition.get_alphabet() == alphabet]

    def create_combined_state(self, next_states):
        sorted_names = sorted(state.name for state in next_states)
        new_state_name = "".join(sorted_names)

        for state in self.handled_states | self.unhandled_states:
            if state.name == new_state_name:
                return state

        new_state = State(new_state_name)
        if any(self.nfa.get_state_type(state) == StateType.FINAL for state in next_states):
            self.nfa.add_final_state(new_state)

        for state in next_states:
            for transition in state.get_transitions():
                new_state.add_transition(transition)

        self.unhandled_states.add(new_state)
        return new_state

    def process_unhandled_states(self):
        while self.unhandled_states:
            state = self.unhandled_states.pop()
            self.add_table_row(state)

    def convert_to_nfa(self, epsilon_nfa):
        converted_nfa = NFA()
        initial_state = State(epsilon_nfa.get_initial_state().name)
        converted_nfa.add_state(initial_state)
        converted_nfa.set_initial_state(initial_state)

        for curr in epsilon_nfa.get_states():
            current_state = converted_nfa.get_state_by_name(curr.name)
            if current_state:
                for symbol in epsilon_nfa.get_alphabets():
                    epsilon = set()
                    next_states = []

                    for state in self.get_epsilon_closure(curr):
                        next_states.extend(self.get_next_states_for_alphabet(state, symbol))

                    for next_state in next_states:
                        epsilon.update(self.get_epsilon_closure(next_state))

                    for state in epsilon:
                        new_state = converted_nfa.get_state_by_name(state.name)
                        if symbol != 'e':
                            converted_nfa.add_transition(current_state, symbol, new_state)
                            if epsilon_nfa.get_state_type(state) == StateType.FINAL:
                                converted_nfa.add_final_state(new_state)

        return converted_nfa

    def get_epsilon_closure(self, state):
        epsilon_closure = set()
        visited = set()
        stack = deque([state])

        while stack:
            current_state = stack.pop()
            if current_state not in visited:
                visited.add(current_state)
                epsilon_closure.add(current_state)

                for transition in current_state.get_transitions():
                    if transition.get_alphabet() == 'e':
                        stack.append(transition.get_next_state())

        return epsilon_closure

    def is_state_exist(self, states, state):
        return any(s.name == state.name for s in states)

    def add_phi_row(self):
        phi = State(self.PHI)
        row = [phi] * (len(self.nfa.get_alphabets()) + 1)
        self.transition_table.append(row)