
class State:
    def __init__(self, name):
        self.name = name
        self.transitions = []

    def get_name(self) -> str:
        return self.name

    def add_transition(self, transition) -> None:
        if not self.is_transition_exist(transition):
            self.transitions.append(transition)

    def get_transitions(self) -> list:
        return self.transitions
    
    def is_transition_exist(self, transition) -> bool:
        return any(
            t.get_alphabet() == transition.get_alphabet()
            and t.get_next_state() == transition.get_next_state()
            for t in self.transitions
        )

    def __str__(self):
        return self.name
