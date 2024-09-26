class Transition:
    def __init__(self, alphabet: str, next_state: 'State'):
        self.alphabet = alphabet
        self.next_state = next_state

    def get_alphabet(self) -> str:
        return self.alphabet

    def get_next_state(self) -> 'State':
        return self.next_state

    def set_next_state(self, next_state) -> None:
        self.next_state = next_state

    def __str__(self):
        if self.alphabet == 'e':
            return f"e -> {self.next_state}"
        return f"{self.alphabet} -> {self.next_state}"
