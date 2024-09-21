import re
import utils

def get_transitions(txt):
    transitions = {}
    pattern = r'Transitions from (\w+|\?):\n((?:\s+\w+ -> (\w+|\?)\n?)+)'

    # Join the list into a single string with line breaks
    combined_txt = '\n'.join(txt)

    for match in re.findall(pattern, combined_txt):
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

    return result

def handle_dfa(output_text):
    lines = output_text.split('\n')
    lines = lines[lines.index('DFA:')+1:]
    lines = lines[:lines.index('')]
    
    result = [
        lines[0].strip().split(': ')[1][1:-1],
        lines[1].strip().split(': ')[1][1:-1],
        lines[2].strip().split(': ')[1],
        lines[3].strip().split(': ')[1][1:-1]]
    
    return result + convert_format(get_transitions(lines[4:]))
    