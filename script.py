import subprocess
import os

def get_dfa_output():
    # Specify the directory where the .class files are located (e.g., 'bin')
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static', 'output' ,'nfa.txt'))
    class_directory = r"static\nfa_to_dfa"

    # Specify the main class name (the class with the 'main()' method)
    main_class_name = "Main"  # Replace this with the actual main class name

    # Step 1: Run the main class using the .class files
    run_command = ["java", "-cp", class_directory, main_class_name, file_path]
    run_process = subprocess.run(run_command, capture_output=True, text=True)

    # Output the result from running the Java program
    print("Java program output")
    # print(run_process.stdout)

    # Check for any errors during execution
    if run_process.stderr:
        print("Error during execution:")
        print(run_process.stderr)


# get_dfa_output()