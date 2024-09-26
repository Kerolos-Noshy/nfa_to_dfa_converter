from .state import State
from .finite_automata import FiniteAutomata
from .state_type import StateType
from .transition import Transition


class NFA(FiniteAutomata):
    def __init__(self):
        super().__init__()
        self.has_epsilon = False

    def add_transition(self, from_state, alphabet, to_state):
        if alphabet == self.EPSILON:
            self.has_epsilon = True
            self.alphabets.add(self.EPSILON)
        else:
            self.alphabets.add(alphabet)
        from_state.add_transition(Transition(alphabet, to_state))

    def get_state_type(self, state):
        if self.get_initial_state() == state:
            return StateType.INITIAL
        elif state in self.final_states:
            return StateType.FINAL
        return None

    def get_state_by_name(self, name):
        # If the state exists, return it; otherwise, create and return a new state
        for state in self.states:
            if state.get_name() == name:
                return state

        new_state = State(name)
        self.add_state(new_state)
        return new_state

    def has_epsilon(self):
        return self.has_epsilon
    
    def get_next_state_for_alphabet(self, state, alphabet):
        return next(
            (
                transition.get_next_state()
                for transition in state.get_transitions()
                if transition.get_alphabet() == alphabet
            ),
            None,
        )
    
    def get_transitions(self):
        transitions = []
        for state in self.get_states():
            for alphabet in self.get_alphabets():
                next_state = self.get_next_state_for_alphabet(state, alphabet)
                if next_state is not None:
                    transitions.append([state.get_name(), alphabet, next_state.get_name()])
        return transitions

    def __str__(self):
        return "NFA:\n" + super().__str__()
