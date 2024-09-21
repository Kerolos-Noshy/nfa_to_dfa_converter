import graphviz
import utils

def convert_format(input_dict):
    result = []

    for state, transitions in input_dict.items():
        result.extend(
            [state, symbol, next_state]
            for symbol, next_state in transitions.items()
        )

    return result

def create_graph(type, transitions, start_state, accept_states):
    dot = graphviz.Digraph(comment=type)
    dot.attr('graph', charset='UTF-8')
    dot.attr(size='6,6', dpi='70', ratio='fill', scale='0.75')
    transitions = convert_format(transitions)
    accept_states = [s.replace('?', 'Ø') for s in accept_states]
    states = list({s.replace('?', 'Ø') for _, _, s in transitions} | {x.replace('?', 'Ø') for x, _, _ in transitions})
    
    unique_states = set() 
    for state in states:
        if ',' in state:
            # Split the state by commas
            next_states = state.split(',')
            for next_state in next_states:
                # Add the next state if it doesn't already exist
                unique_states.add(next_state.strip())  # Use strip() to remove any extra spaces
        else:
            unique_states.add(state)
# Convert back to list if needed
    for state in unique_states:  # Use list to avoid modifying the set during iteration
        if state in accept_states:
            dot.node(state, shape='doublecircle') 
        else:
            dot.node(state)
        

    # Add start state marker
    dot.node('', shape='none')  # Invisible starting point
    dot.edge('', start_state)   # Edge pointing to start state

    for state, symbol, next_state in transitions:
        label= 'ε' if symbol == 'e' else symbol
        # state = state.replace('?', 'Ø')
        next_state = next_state.replace('?', 'Ø')
        if next_state in unique_states:
            
            dot.edge(state.replace('?', 'Ø'), next_state.replace('?', 'Ø'), label=label)
        else:
            next_states = next_state.split(',')

            for next_state in next_states:
                dot.edge(state.replace('?', 'Ø'), next_state, label=label)


    return dot.render(f'{utils.OUTPUT_FOLDER}/{type}_graph', view=False, format='svg', cleanup=True)