def get_states(txt):
    # match = re.search(r'\[(.*?)\]', txt[0])

    # states = match.group(1).replace('˜', '').replace('Ã', 'Ø')
    states = txt[0].split(',')
    states = [state.strip() for state in states]
    return states

def get_alphabets(txt: list[str]):

    # match = re.search(r'\[(.*?)\]', txt[1])

    # alphabets = match.group(1).replace('e', 'ε')
    alphabets = txt[1].replace('e', 'ε').split(',')
    alphabets = [alphabet.strip() for alphabet in alphabets]
    return alphabets

def get_initial_state(txt):
    # match = re.search(r'Initial State: (\d+)', txt[2])

    # initial_state = match.group(1)
    return txt[2].strip()

def get_accepting_states(txt):
    # match = re.search(r'Accepting States: \[(.*?)\]', txt[3])

    # accepting_states = match.group(1)
    accepting_states = txt[3].split(',')
    accepting_states = [state.strip() for state in accepting_states]
    return accepting_states


def get_transitions(txt):
    transitions = {}

    for line in txt[4:]:
        transition_parts = [part.strip() for part in line.split(',')]
        
        # Each transition should have 3 parts: from_state, symbol, to_state
        if len(transition_parts) == 3:
            from_state, symbol, to_state = transition_parts

            # Initialize the dictionary for this state if it doesn't exist
            if from_state not in transitions:
                transitions[from_state] = {}

            # Add the transition
            if symbol not in transitions[from_state]:
                transitions[from_state][symbol] = []

            if to_state not in transitions[from_state][symbol]:
                transitions[from_state][symbol].append(to_state)
            
    # sort the to_states list in each transition
    transitions = {state: {symbol: sorted(to_states) for symbol, to_states in symbols.items()} for state, symbols in transitions.items()}
        
    for state, symbols in transitions.items():
        for symbol, to_states in symbols.items():
            transitions[state][symbol] = ','.join(to_states)
    return transitions