public class Transition {
    private char alphabet;
    private State nextState;

    public Transition(char alphabet, State nextState) {
        this.alphabet = alphabet;
        this.nextState = nextState;
    }

    public char getAlphabet() {
        return alphabet;
    }

    public State getNextState() {
        return nextState;
    }

    public void setNextState(State nextState) {
        this.nextState = nextState;
    }

    @Override
    public String toString() {
        if (alphabet == 'e')
            return "e" + " -> " + nextState;
        return alphabet + " -> " + nextState;
    }
}
