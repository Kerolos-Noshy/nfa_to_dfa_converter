import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.Set;

public abstract class FiniteAutomata {
    protected Set<State> states;
    protected Set<Character> alphabets;
    protected State initialState;
    protected Set<State> finalStates;
    protected final char EPSILON;

    FiniteAutomata() {
        this.states = new LinkedHashSet<>();
        this.alphabets = new HashSet<>();
        this.finalStates = new HashSet<>();
        this.EPSILON = 'e';
    }

    protected boolean isStateExist(State state){
        for (State s:states)
            if (s.getName().equals(state.getName()))
                return true;
        return false;
    }

    protected boolean isStateExist(String state){
        for (State s:states)
            if (s.getName().equals(state))
                return true;
        return false;
    }

    public void addState(State state) {
        if (!isStateExist(state))
            states.add(state);
        else
            System.out.println("State" + state.getName() + "already exist");
    }

    public void addStates(String[] statesArray) {
        for (String state:statesArray) {
            if (!isStateExist(state))
                states.add(new State(state));
            else
                System.out.println("State " + state + " already exist");
        }
    }

    public Set<State> getStates() {
        return states;
    }

    public Set<Character> getAlphabets() {
        return alphabets;
    }

    public void setAlphabets(Set<Character> alphabets) {
        this.alphabets = alphabets;
    }

    public State getInitialState() {
        return initialState;
    }

    public void setInitialState(State initialState) {
        this.initialState = initialState;
    }

    public Set<State> getFinalStates() {
        return finalStates;
    }

    public void addFinalState(State finalState) {
        finalStates.add(finalState);
    }

    public State getStateByName(String name){
        for(State state: states)
            if (state.getName().equals(name))
                return state;

        return null;
    }

    @Override
    public String toString(){
        return null;
    };
}
