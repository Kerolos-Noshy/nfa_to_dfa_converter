import re
import utils

def get_transitions(txt):
    transitions = {}

    pattern = r'Transitions from (\w+):\n((?:\s+\w+ -> (\w|\?)+\n?)*)'
    

    for match in re.findall(pattern, ''.join(txt)):
        state = match[0].strip()
        trans = match[1].strip().split('\n')
        transitions[state] = {t.split(' -> ')[0].strip(): t.split(' -> ')[1].strip() for t in trans}

    return transitions



def convert_format(input_dict):
    result = []

    for state, transitions in input_dict.items():
        result.extend(
            f"{state}, {symbol}, {next_state}"
            for symbol, next_state in transitions.items()
        )

    return "\n".join(result)

def handle_dfa():
    with open(f'{utils.OUTPUT_FOLDER}/dfa.txt', 'r') as f:
        lines = f.readlines()

    lines = lines[lines.index('DFA:\n')+1:]


    with open(f'{utils.OUTPUT_FOLDER}/dfa_formated.txt', 'w') as f:
        f.write(lines[0].strip().split(': ')[1][1:-1] + '\n')
        f.write(lines[1].strip().split(': ')[1][1:-1] + '\n')
        f.write(lines[2].strip().split(': ')[1] + '\n')
        f.write(lines[3].strip().split(': ')[1][1:-1] + '\n')
        f.writelines(convert_format(get_transitions(lines[4:])))

