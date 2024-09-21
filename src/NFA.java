import java.util.*;

public class NFA extends FiniteAutomata{

    private boolean hasEpsilon;

    public NFA() {
        super();
        this.hasEpsilon = false;
    }

    //    public enum StateType {INITIAL, FINAL}


    public void addTransition(State fromState, char alphabet, State toState) {
        if (alphabet == EPSILON) {
            hasEpsilon = true;
            alphabets.add(EPSILON);
        }
        else
            alphabets.add(alphabet);
        fromState.addTransition(new Transition(alphabet, toState));

    }

    public StateType getStateType(State state){
        if (this.getInitialState() == state)
            return StateType.INITIAL;

        else if (finalStates.contains(state))
            return StateType.FINAL;

        return null;
    }

    @Override
    public State getStateByName(String name){
        // if state exist return it else create new state and return it
        for(State state: states)
            if (state.getName().equals(name))
                return state;

        State newState = new State(name);
        this.addState(newState);
        return newState;

    }

//    public void sortAllTransitions() {
//        for(State s: states)
//            s.sortTransitions();
//    }

    public boolean hasEpsilon() {
        return hasEpsilon;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("NFA:\n");
        sb.append("States: ").append(states).append("\n");
        sb.append("Alphabet: ").append(alphabets).append("\n");
        sb.append("Initial State: ").append(initialState).append("\n");
        sb.append("Accepting States: ").append(finalStates).append("\n");
        for (State state : states) {
            if (!state.getTransitions().isEmpty()) {
                sb.append("Transitions from ").append(state).append(":\n");
                for (Transition transition : state.getTransitions())
                    sb.append("  ").append(transition).append("\n");

            }
        }
        return sb.toString();
    }
}
