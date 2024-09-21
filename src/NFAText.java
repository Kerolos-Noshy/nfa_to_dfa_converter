import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class NFAText {
    public static NFA getNFAFromFile(String filePath) throws IOException {
        NFA nfa = new NFA();
        BufferedReader reader = new BufferedReader(new FileReader(filePath));
        String line;

        line = reader.readLine();
        String[] stateNames = line.split(",");
        List<State> states = new ArrayList<>();
        for (String name : stateNames) {
            State state = new State(name.trim());
            nfa.addState(state);
            states.add(state);
        }

        // Read the alphabet
        line = reader.readLine();
        String[] alphabet = line.split(",");


        // Read the start state
        line = reader.readLine();

        State startState = getStateByName(states, line.trim());
        nfa.setInitialState(startState);

        // Read the final states
        line = reader.readLine();
        String[] finalStateNames = line.split(",");
        for (String name : finalStateNames) {
            State finalState = getStateByName(states, name.trim());
            nfa.addFinalState(finalState);
        }

        while ((line = reader.readLine()) != null) {
            String[] transitionParts = line.split(",");
            State fromState = getStateByName(states, transitionParts[0].trim());
            char symbol = transitionParts[1].trim().charAt(0);
            State toState = getStateByName(states, transitionParts[2].trim());
            nfa.addTransition(fromState, symbol, toState);
        }

        reader.close();
        return nfa;
    }
    private static State getStateByName(List<State> states, String name) {
        for (State state : states) {
            if (state.getName().equals(name)) {
                return state;
            }
        }
        return null;
    }
}
