from .finite_automata import FiniteAutomata
from .state_type import StateType
from .transition import Transition
from .state import State

class DFA(FiniteAutomata):
    def __init__(self):
        super().__init__()

    def add_transition(self, from_state, alphabet, to_state):
        self.alphabets.add(alphabet)
        from_state.add_transition(Transition(alphabet, to_state))

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

    def is_equivalent(self, previous_eq, state1, state2):
        for alphabet in self.get_alphabets():
            for group in previous_eq:
                if (
                    self.get_next_state_for_symbol(state1, alphabet) in group
                    and self.get_next_state_for_symbol(state2, alphabet) in group
                ):
                    return True
        return False

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
        output = []
        previous_equivalence = [[], []]
        for state in self.get_states():
            if state.get_name() != '?':
                if state not in self.get_final_states():
                    previous_equivalence[0].append(state)
                else:
                    previous_equivalence[1].append(state)

        current_equivalence = self.get_next_equivalence(previous_equivalence)
        i = 0
        output.append(f"{i} - Equivalence: {[[state.get_name() for state in l]for l in previous_equivalence]}")
        while len(current_equivalence) != len(previous_equivalence):
            output.append(f"{i + 1} - Equivalence: {[[state.get_name() for state in l]for l in current_equivalence]}")
            previous_equivalence = current_equivalence
            current_equivalence = self.get_next_equivalence(previous_equivalence)
            i += 1
        output.append(f"{i + 1} - Equivalence: {[[state.get_name() for state in l]for l in current_equivalence]}")
        return output

    def get_transitions(self):
        transitions = []
        for state in self.get_states():
            for alphabet in self.get_alphabets():
                next_state = self.get_next_state_for_alphabet(state, alphabet)
                if next_state is not None:
                    transitions.append([state.get_name(), alphabet, next_state.get_name()])
        return transitions

    def __str__(self):
        sb = [
            "DFA:\n",
            f"States: {[state.get_name() for state in self.states]}\n",
            f"Alphabet: {self.alphabets}\n",
            f"Initial State: {self.initial_state}\n",
            f"Accepting States: {[state.get_name() for state in self.final_states]}\n",
        ]
        for state in self.states:
            if state.get_transitions():
                sb.append(f"Transitions from {state}:\n")
                sb.extend(f"  {transition}\n" for transition in state.get_transitions())
        return "".join(sb)
