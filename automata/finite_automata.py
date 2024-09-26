from abc import ABC, abstractmethod
from .state import State


class FiniteAutomata(ABC):
    def __init__(self):
        self.states: list[State] = []
        self.alphabets: set[str] = set()
        self.initial_state: State | None = None
        self.final_states: set[State] = set()
        self.EPSILON = 'e'

    def is_state_exist(self, state: State) -> bool:
        if isinstance(state, State):
            return any(s.get_name() == state.get_name() for s in self.states)
        elif isinstance(state, str):
            return any(s.get_name() == state for s in self.states)
        return False

    def add_state(self, state: State) -> None:
        if not self.is_state_exist(state):
            self.states.append(state)

    def add_states(self, states_list: list[State]) -> None:
        for state in states_list:
            if not self.is_state_exist(state):
                self.states.append(state)

    def get_states(self) -> list[State]:
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

    def get_final_states(self) -> set[State]:
        return self.final_states

    def add_final_state(self, final_state: State) -> None:
        if final_state not in self.final_states:
            self.final_states.add(final_state)

    def get_state_by_name(self, name: str) -> State:
        return next((state for state in self.states if state.get_name() == name), None)

    @abstractmethod
    def get_transitions(self):
        pass

    @abstractmethod
    def __str__(self):
        sb = [
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