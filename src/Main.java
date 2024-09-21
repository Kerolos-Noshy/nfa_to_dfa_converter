import java.io.*;
import java.util.Arrays;
import java.util.List;

public class Main {
    public static void print(String s){
        System.out.println(s);
    }


    public static void main(String[] args) {
        args[0] = "C:\\Users\\kerol\\Desktop\\nfa to dfa - streamlit\\NFA_TO_DFA_java\\python\\static\\output\\nfa.txt";
        NFA nfa = null;
        String[] splitPath = args[0].split("\\\\");

        // Join all elements except the last one
        String joinedPath = String.join("\\", Arrays.copyOf(splitPath, splitPath.length - 1));


        try {
            String file_path = args[0];
            nfa = NFAText.getNFAFromFile(file_path);
            print(nfa.toString());
        } catch (IOException e) {
            e.printStackTrace();
        }
        System.out.println("-----");

        AutomataConverter converter = new AutomataConverter(nfa, true);
        DFA dfa = converter.convertToDFA(true);
        System.out.println(dfa);
        saveOutputToTxtFile(nfa + "\n-----\n" + dfa.toString(), joinedPath, "dfa.txt");

        printDFATransitionTable(dfa);
        print(dfa.minimize());
        saveOutputToTxtFile(dfa.minimize(), joinedPath, "minimized_dfa.txt");
    }

    public static void printDFATransitionTable(DFA dfa){
        System.out.println("--- Transition Table ---");
        System.out.print("\tState \t");
        StringBuilder sb = new StringBuilder();
        for (char s:dfa.getAlphabets())
            sb.append(s).append("\t\t");
        sb.setLength(sb.length()-2);
        System.out.println(sb.append("\t"));

        System.out.println("--------------------------");

        for (State state: dfa.getStates()) {
            if (dfa.getFinalStates().contains(state))
                System.out.print("  * ");
            else if (dfa.getInitialState().getName().equals(state.getName()))
                System.out.print("  > ");
            else
                System.out.print("\t");

            System.out.print(state.getName() + "\t\t");
            for (char alpha: dfa.getAlphabets())
                System.out.print(dfa.getNextStatesForAlphabet(state, alpha) + "\t\t");

            System.out.println();
        }
        System.out.println();
    }

    public static void saveOutputToTxtFile(String text, String path, String fileName) {
        // The file where output will be saved
        String filename = path + "\\" + fileName;

        try {
            // Create a FileWriter object to write to the file (append mode: true)
            FileWriter writer = new FileWriter(filename);

            // Write output to the file
            writer.write(text);

            // Close the writer to save the file
            writer.close();

            System.out.println("Output saved to " + filename);
        } catch (IOException e) {
            System.out.println("An error occurred while saving the file.");
            e.printStackTrace();
        }
    }
}



