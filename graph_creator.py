import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from automata import FiniteAutomata


def create_graph(title, automata: FiniteAutomata):
    transitions = automata.get_transitions()
    start_state = automata.get_initial_state().get_name()
    accept_states = {state.get_name() for state in automata.get_final_states()}

    G = nx.MultiDiGraph()  # MultiDiGraph allows parallel edges

    # Dictionary to hold transitions with the same (src, dst) without overriding
    transition_dict = defaultdict(list)

    # Group transitions by (src, dst) and combine their symbols
    for src, symbol, dst in transitions:
        transition_dict[(src, dst)].append(symbol)

    # Add transitions to the graph, joining symbols with commas if multiple exist
    for (src, dst), symbols in transition_dict.items():
        combined_symbols = ','.join(symbols)  # Join multiple symbols with commas
        G.add_edge(src, dst, label=combined_symbols)

    # Prepare for drawing
    pos = nx.spring_layout(G)

    plt.figure(figsize=(8, 6))

    # Draw the basic graph structure
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=700)
    nx.draw_networkx_edges(G, pos, arrowsize=20, connectionstyle='arc3,rad=0.1')  # This adds a slight arc
    nx.draw_networkx_labels(G, pos)

    # Highlight start state
    nx.draw_networkx_nodes(G, pos, nodelist=[start_state], node_color='lightgreen', node_size=700)

    # Highlight final states
    try:
        nx.draw_networkx_nodes(G, pos, nodelist=accept_states, node_color='lightpink', node_size=700)
    except nx.NetworkXException:
        # Final state doesn't have any transitions
        pass

    # Draw edge labels for all transitions
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Remove the axis
    plt.axis('off')
    plt.title(title)

    # Return the figure object
    return plt.gcf()

# import graphviz

# def create_graph(type, transitions, start_state, accept_states):
#     dot = graphviz.Digraph(comment=type)
#     dot.attr('graph', charset='UTF-8')
#     dot.attr(size='6,6', dpi='70', ratio='fill', scale='0.75')
#     accept_states = [s.replace('?', 'Ø') for s in accept_states]
#     states = list({s.replace('?', 'Ø') for _, _, s in transitions} | {x.replace('?', 'Ø') for x, _, _ in transitions})
#
#     unique_states = set()
#     for state in states:
#         if ',' in state:
#             # Split the state by commas
#             next_states = state.split(',')
#             for next_state in next_states:
#                 # Add the next state if it doesn't already exist
#                 unique_states.add(next_state.strip())  # Use strip() to remove any extra spaces
#         else:
#             unique_states.add(state)
# # Convert back to list if needed
#     for state in unique_states:  # Use list to avoid modifying the set during iteration
#         if state in accept_states:
#             dot.node(state, shape='doublecircle')
#         else:
#             dot.node(state)
#
#
#     # Add start state marker
#     dot.node('', shape='none')  # Invisible starting point
#     dot.edge('', start_state)   # Edge pointing to start state
#
#     for state, symbol, next_state in transitions:
#         label= 'ε' if symbol == 'e' else symbol
#         # state = state.replace('?', 'Ø')
#         next_state = next_state.replace('?', 'Ø')
#         state = state.replace('?', 'Ø')
#         if next_state in unique_states:
#
#             dot.edge(state, next_state, label=label)
#         else:
#             next_states = next_state.split(',')
#
#             for next_state in next_states:
#                 dot.edge(state, next_state, label=label)
#
#     svg_output = dot.pipe(format='svg').decode('utf-8')
#     return svg_output
#     # return dot.render(f'{utils.OUTPUT_FOLDER}/{type}_graph', view=False, format='svg', cleanup=True)