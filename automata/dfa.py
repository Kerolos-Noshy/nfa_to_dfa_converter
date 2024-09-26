from .finite_automata import FiniteAutomata
from .state_type import StateType
from .transition import Transition
from .state import State


class DFA(FiniteAutomata):
    def __init__(self):
        super().__init__()
        self.PHI = 'Ø'

    def add_transition(self, from_state, alphabet, to_state):
        if alphabet != self.EPSILON:
            self.alphabets.add(alphabet)
            from_state.add_transition(Transition(alphabet, to_state))

    def remove_transition(self, state: State, transition: Transition):
        state.remove_transition(transition)

    @staticmethod
    def get_next_state_for_symbol(state, alphabet):
        return next(
            (
                transition.get_next_state()
                for transition in state.get_transitions()
                if transition.get_alphabet() == alphabet
            ),
            None,
        )

    def get_state_type(self, state):
        if self.get_initial_state() == state:
            return StateType.INITIAL
        elif state in self.final_states:
            return StateType.FINAL
        return None

    def get_next_state_for_alphabet(self, state, alphabet):
        return next(
            (
                transition.get_next_state()
                for transition in state.get_transitions()
                if transition.get_alphabet() == alphabet
            ),
            None,
        )

    def is_string_accepted(self, s):
        # Check if a given string is accepted (reaches a final state) in the machine
        current_state = self.get_initial_state()
        for c in s:
            current_state = self.get_next_state_for_symbol(current_state, c)
        return current_state in self.get_final_states()

    def states_in_same_group(self, states_groups, s1, s2):
        for group in states_groups:
            group_str = list(map(str, group))
            if s1 in group_str and s2 in group_str:
                return True
        return False

    def is_equivalent(self, previous_eq, state1, state2):
        for group in previous_eq:
            if len(group) > 1:
                equivalent_alphabets = []
                for alphabet in self.get_alphabets():
                    next1 = str(self.get_next_state_for_symbol(state1, alphabet))
                    next2 = str(self.get_next_state_for_symbol(state2, alphabet))
                    equivalent_alphabets.append(self.states_in_same_group(previous_eq, next1, next2))

                return all(equivalent_alphabets)

    def get_next_equivalence(self, previous_eq):
        next_equivalence = []

        for group in previous_eq:
            if len(group) == 1:
                next_equivalence.append(group)
            else:
                for state in group:
                    if not next_equivalence:
                        next_equivalence.append([group[0]])
                    else:
                        flag = False
                        for next_group in next_equivalence:
                            if self.is_equivalent(previous_eq, state, next_group[0]):
                                next_group.append(state)
                                flag = True
                                break
                        if not flag:
                            next_equivalence.append([state])

        return next_equivalence

    def minimize(self):
        equivalence_list = []
        previous_equivalence = [[], []]
        for state in self.get_states():
            if state.get_name() != self.PHI:
                if state not in self.get_final_states():
                    previous_equivalence[0].append(state)
                else:
                    previous_equivalence[1].append(state)
        equivalence_list.append(previous_equivalence)
        current_equivalence = self.get_next_equivalence(previous_equivalence)
        while len(current_equivalence) != len(previous_equivalence):
            equivalence_list.append(current_equivalence)
            previous_equivalence = current_equivalence
            current_equivalence = self.get_next_equivalence(previous_equivalence)

        return equivalence_list

    def print_minimization(self):
        equivalence_list = self.minimize()
        output = []
        for i, current_equivalence in enumerate(equivalence_list):
            output.append(f"{i} - Equivalence: {[[state.get_name() for state in l] for l in current_equivalence]}")
        return output

    def convert_minimization_to_DFA(self, minimized_states):
        def get_equivalent_state(state, removed_states_dict):
            for k, v in removed_states_dict.items():
                if state in v:
                    return k

        removed_states_dict = dict()
        removed_states = []
        minimized_DFA = DFA()
        minimized_DFA.alphabets = set(sorted(self.get_alphabets()))
        for group in minimized_states:
            if len(group) > 1:
                removed_states.extend([str(s) for s in group])
        for group in minimized_states:
            if len(group) == 1:
                state = group[0]
                if str(state) not in removed_states:
                    for transition in state.get_transitions():
                        if transition.get_next_state().get_name() in removed_states:
                            state.remove_transition(transition)
                            state.add_transition(Transition(transition.get_alphabet(),
                                                                get_equivalent_state(str(transition.get_next_state()), removed_states_dict)))
                        else:
                            state.add_transition(transition)
                    minimized_DFA.add_state(state)
                    if self.get_state_type(state) == StateType.INITIAL:
                        minimized_DFA.set_initial_state(state)
                    elif self.get_state_type(state) == StateType.FINAL:
                        minimized_DFA.add_final_state(state)
            else:
                new_state = State(''.join(map(str, group)))

                for state in group:

                        if self.get_state_type(state) == StateType.INITIAL:
                            minimized_DFA.set_initial_state(new_state)
                        elif self.get_state_type(state) == StateType.FINAL:
                            minimized_DFA.add_final_state(new_state)
                        removed_states_dict[new_state] = [str(s) for s in group]
                        for transition in state.get_transitions():
                            if transition.get_next_state().get_name() in removed_states:
                                new_state.add_transition(Transition(transition.get_alphabet(),
                                                                    get_equivalent_state(str(state), removed_states_dict)))
                            else:
                                new_state.add_transition(transition)
                minimized_DFA.add_state(new_state)

        return minimized_DFA




    def get_transitions(self):
        transitions = []
        for state in self.get_states():
            for alphabet in self.get_alphabets():
                if alphabet != self.EPSILON:
                    next_state = self.get_next_state_for_alphabet(state, alphabet)
                    if next_state is not None:
                        transitions.append([state.get_name(), alphabet, next_state.get_name()])
        return transitions

    def __str__(self):
        return "DFA:\n" + super().__str__()
