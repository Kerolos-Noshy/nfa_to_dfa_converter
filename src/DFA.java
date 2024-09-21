import java.util.*;

public class DFA extends FiniteAutomata{

    public DFA() {
        super();
    }
    public void addTransition(State fromState, char alphabet, State toState) {
        alphabets.add(alphabet);
        fromState.addTransition(new Transition(alphabet, toState));
    }

    public static State getNextStateForSymbol(State state, char alphabet) {
        for (Transition transition : state.getTransitions()) {
            if (transition.getAlphabet() == alphabet) {
                return transition.getNextState();
            }
        }
        return null;
    }

    public StateType getStateType(State state){
        if (this.getInitialState() == state)
            return StateType.INITIAL;

        else if (finalStates.contains(state))
            return StateType.FINAL;

        return null;
    }

    public State getNextStatesForAlphabet(State state, char alphabet) {
        for (Transition transition : state.getTransitions()) {
            if (transition.getAlphabet() == alphabet) {
                return transition.getNextState();
            }
        }
        return null;
    }

    public boolean isStringAccepted(String s){
        // check if a given string is accepted (reach a final state) in the machine
        State currentState = getInitialState();
        for (char c:s.toCharArray()){
            currentState = getNextStateForSymbol(currentState, c);
        }
        return getFinalStates().contains(currentState);
    }


    private boolean is_equivalent(List<List<State>> previous_eq, State state1, State state2) {
        boolean equivalent_flag = false;
        for (char alphabet:getAlphabets()){
            for (List<State> list: previous_eq) {
                if (list.contains(getNextStateForSymbol(state1, alphabet))
                        && list.contains(getNextStateForSymbol(state2, alphabet))) {
                    equivalent_flag = true;
                    break;
                }
            }
            if (!equivalent_flag)
                return false;
            else
                equivalent_flag = false;
        }

        return true;
    }

    private List<List<State>> getNextEquivalence(List<List<State>> previous_eq){
        List<List<State>> nextEquivalence = new ArrayList<>();

        for (List<State> list: previous_eq){
            if (list.size() == 1) {
                nextEquivalence.add(list);
            }
            else {
                for (State state : list) {
                    if (nextEquivalence.isEmpty()) {
                        List<State> newList = new ArrayList<>();
                        newList.add(list.get(0));
                        nextEquivalence.add(newList);
                    } else {
                        boolean flag = false;
                        for (List<State> groupList : nextEquivalence) {
                            if (is_equivalent(previous_eq, state, groupList.get(0))) {
                                groupList.add(state);
                                flag = true;
                                break;
                            }
                        }
                        if (!flag) {
                            List<State> newList = new ArrayList<>();
                            newList.add(state);
                            nextEquivalence.add(newList);
                        }
                    }
                }
            }
        }

        return nextEquivalence;
    }

    public String minimize(){
        StringBuilder output = new StringBuilder();
        List<List<State>> previous_equivalence = new ArrayList<>();
        previous_equivalence.add(new ArrayList<>());
        previous_equivalence.add(new ArrayList<>());
        for(State state:this.getStates()) {
            if (!state.getName().equals("?")) {
                if (!getFinalStates().contains(state))
                    previous_equivalence.get(0).add(state);
                else
                    previous_equivalence.get(1).add(state);
            }
        }

        List<List<State>> current_equivalence = getNextEquivalence(previous_equivalence);
        int i = 0;
        output.append(i).append("- Equivalence: ").append(previous_equivalence).append('\n');
//        System.out.println(i + "- Equivalence: " + previous_equivalence);
        while (current_equivalence.size() != previous_equivalence.size()){
            output.append(++i).append("- Equivalence: ").append(current_equivalence).append('\n');
//            System.out.println(++i + "- Equivalence: " + current_equivalence);
            previous_equivalence = current_equivalence;
            current_equivalence = getNextEquivalence(previous_equivalence);
        }
        output.append(++i).append("- Equivalence: ").append(current_equivalence);
//        System.out.println(++i + "- Equivalence: " + current_equivalence);

        return String.valueOf(output);
    }


    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("DFA:\n");
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
