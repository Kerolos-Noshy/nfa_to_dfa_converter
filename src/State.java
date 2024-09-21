import java.util.*;

public class State {
    private String name;
    private List<Transition> transitions;
//    private StateType stateType;

    public State(String name) {
        this.name = name;
        this.transitions = new ArrayList<>();
//        this.stateType = StateType.NORMAL;
    }

    public String getName() {
        return name;
    }

    public void addTransition(Transition transition) {
        if (!isTransitionExist(transition))
            transitions.add(transition);
    }

    public List<Transition> getTransitions() {
        return transitions;
    }

//    public StateType getStateType() {
//        return stateType;
//    }
//
//    public void setStateType(StateType stateType) {
//        this.stateType = stateType;
//    }

    public void sortTransitions() {
        this.transitions.sort(Comparator
                .comparing(Transition::getAlphabet)
                .thenComparing(transition -> transition.getNextState().getName()));
    }

    private boolean isTransitionExist(Transition transition) {
        for (Transition t: transitions) {
            if (t.getAlphabet() == transition.getAlphabet() && transition.getNextState() == t.getNextState())
                return true;
        }
        return false;
    }

    @Override
    public String toString() {
        return name;
    }

    //    public enum StateType {
//        NORMAL,
//        INITIAL,
//        ACCEPTING
//    }
}