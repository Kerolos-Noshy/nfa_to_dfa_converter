from abc import ABC, abstractmethod
from .state import State

class FiniteAutomata(ABC):
    def __init__(self):
        self.states = []
        self.alphabets = set()
        self.initial_state = None
        self.final_states = set()
        self.EPSILON = 'e'

    def is_state_exist(self, state) -> bool:
        if isinstance(state, State):
            return any(s.get_name() == state.get_name() for s in self.states)
        elif isinstance(state, str):
            return any(s.get_name() == state for s in self.states)
        return False

    def add_state(self, state) -> None:
        if not self.is_state_exist(state):
            self.states.append(state)

    def add_states(self, states_array) -> None:
        for state_name in states_array:
            if not self.is_state_exist(state_name):
                self.states.append(State(state_name))


    def get_states(self) -> list:
        return self.states

    def get_alphabets(self) -> set:
        alphabets_list = list(self.alphabets)
        return set(sorted(alphabets_list))

    def set_alphabets(self, alphabets) -> None:
        self.alphabets = alphabets

    def get_initial_state(self) -> State:
        return self.initial_state

    def set_initial_state(self, initial_state) -> None:
        self.initial_state = initial_state

    def get_final_states(self) -> set:
        return self.final_states

    def add_final_state(self, final_state) -> None:
        self.final_states.add(final_state)

    def get_state_by_name(self, name) -> State:
        return next((state for state in self.states if state.get_name() == name), None)

    @abstractmethod
    def __str__(self):
        pass