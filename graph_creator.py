import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def create_graph(transitions, start_state, accept_states:set):
    G = nx.DiGraph()
    # Add all transitions
    for transition in transitions:
        src, symbol, dst = transition
        src = src.replace('?', 'Ø')
        dst = dst.replace('?', 'Ø')
        G.add_edge(src, dst, label=symbol)
    for state in accept_states:
        if state == '?':
            accept_states.remove(state)
            accept_states.add('Ø')

    # Prepare for drawing
    pos = nx.spring_layout(G)

    # Create a new figure
    plt.figure(figsize=(8, 6))

    # Draw the basic graph structure
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=700)
    nx.draw_networkx_edges(G, pos, arrowsize=20)
    nx.draw_networkx_labels(G, pos)

    # Highlight start state
    nx.draw_networkx_nodes(G, pos, nodelist=[start_state], node_color='lightgreen', node_size=700)

    # Highlight final states
    nx.draw_networkx_nodes(G, pos, nodelist=accept_states, node_color='lightpink', node_size=700)

    # Add a dummy node for start state arrow
    dummy_node = 'dummy'
    G.add_node(dummy_node)
    dummy_pos = pos[start_state] - np.array([0.1, 0])
    pos[dummy_node] = dummy_pos
    plt.annotate('', xy=pos[start_state], xytext=dummy_pos,
                 arrowprops=dict(arrowstyle="->", color='green', lw=2))

    # Draw edge labels
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Remove the axis
    plt.axis('off')

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


