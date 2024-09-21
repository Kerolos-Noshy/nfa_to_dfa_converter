import pandas as pd
import streamlit as st
from graph_creator import create_graph
import base64
from automata.nfa import NFA
from automata.automata_converter import AutomataConverter
from automata.state import State

def get_svg_as_base64(img_svg):
    img_svg = img_svg.encode('utf-8') 
    encoded = base64.b64encode(img_svg).decode('utf-8')
    return f'<img src="data:image/svg+xml;base64,{encoded}">'


def get_transitions_table(transitions):
    df = pd.DataFrame(transitions).T
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'State'}, inplace=True)
    df.fillna('', inplace=True)
    return df.rename({'e': "ε"}, axis=1)

def create_transition_table(transitions):
    states = set()
    symbols = set()

    for from_state, symbol, to_state in transitions:
        states.add(from_state)
        states.add(to_state)
        symbols.add(symbol)

    state_list = sorted(map(str, states))

    transition_dict = {state: {symbol: set() for symbol in symbols} for state in state_list}

    for from_state, symbol, to_state in transitions:
        transition_dict[str(from_state)][symbol].add(str(to_state))

    df = pd.DataFrame(columns=symbols)

    for state, symbol_dict in transition_dict.items():
        for symbol, to_states in symbol_dict.items():
            # Convert set of states to a sorted list of strings
            df.at[state, symbol] = ', '.join(sorted(to_states)) if to_states else '∅'
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'State'}, inplace=True)
    return df.replace('?', 'Ø')



def display_states_and_alphabets():
    st.markdown("##### Enter the states (comma-separated):")
    states = st.text_input("Enter the states :red[(comma-separated)]:", "q0,q1,q2", label_visibility='collapsed')
    states = states.split(',')
    states = [state.strip() for state in states]
    # Alphabet input
    # start_state = st.text_input("Enter the start state:", "q0")
    st.markdown("##### Enter the alphabet symbols (comma-separated) :orange[(**enter e for epsilon**)]:")
    alphabets = st.text_input("Enter the alphabet symbols (comma-separated) :orange[(**enter e for epsilon**)]:", "a,b", label_visibility='collapsed')

    alphabets = alphabets.split(',')
    alphabets = [alphabet.strip() for alphabet in alphabets]

    
    return states, alphabets

def display_transition_input(states, alphabets, num_transitions):
    transitions_list = []
    rows = [st.columns(3) for _ in range(num_transitions)]
    
    for i in range(num_transitions):
        with rows[i][0]:
            state = st.selectbox(f"**Transition {i + 1} - From state:**", states)
        with rows[i][1]:
            symbol = st.selectbox(f'**Transition {i + 1} - On symbol:**', alphabets)
        with rows[i][2]:
            next_states = st.selectbox(f"**Transition {i + 1} - To states:**", states)
        
        transitions_list.append((state, symbol, next_states))
    
    return transitions_list

def display_graph_info(graph_type, automata):
    col1, col2 = st.columns(2)
    with col1:
        states = sorted([state.get_name() for state in automata.get_states()])
        if states[0] == '?':
            states.remove('?')
            states.append('?')
        st.latex('''Q (states) =  \{ ''' + ', '.join(states).replace('?', 'Ø') + ''' \}''')
        st.latex('''q_0 (initial \; state) =  \{ ''' + automata.get_initial_state().get_name() + ''' \}''')
    with col2:
        st.latex('''E (alphabets) =  \{ ''' + ', '.join(automata.get_alphabets()).replace('e', 'ε') + ''' \}''')
        st.latex('''F (accepting \; states) =  \{ ''' + ', '.join([accept_state.get_name() for accept_state in automata.get_final_states()]).replace('?', 'Ø') + ''' \}''')
# Function to save data to session state
def save_nfa_to_session(states, alphabets, start_state, accept_states, transitions_list):
    st.session_state.nfa_lines = [
        f"{','.join(states)}\n",
        f"{','.join(alphabets)}\n",
        f"{start_state}\n",
        f"{','.join(accept_states)}\n"
    ] + [f"{s1}, {a}, {s2}\n" for s1, a, s2 in transitions_list]

def create_nfa(states, alphabets, start_state, accept_states, transitions_list):
    nfa = NFA()
    states = [State(state) for state in states]
    for state in states:
        nfa.add_state(state)

    # Set initial and final states
    nfa.set_initial_state(nfa.get_state_by_name(start_state))
    for state in accept_states:
        nfa.add_final_state(nfa.get_state_by_name(state))

    for transition in transitions_list:
        nfa.add_transition(nfa.get_state_by_name(transition[0]), transition[1], nfa.get_state_by_name(transition[2]))

    return nfa

def main():
    st.set_page_config(page_title="NFA to DFA Converter", layout="wide", initial_sidebar_state="auto")
    st.title("NFA to DFA Converter")
    st.header("Input your NFA details")
    
    num_transitions = st.sidebar.number_input("Number of transitions", min_value=1, value=2)
    states, alphabets = display_states_and_alphabets()
    st.markdown("##### Enter the start state:")
    start_state = st.selectbox("Enter the start state:", states, label_visibility='collapsed')


    # accept_states = st.text_input("Enter the accept states (comma-separated):", "q2")
    st.markdown("##### Enter the accept states (multiselect):")
    accept_states = st.multiselect("Enter the accept states (multiselect):", states, label_visibility='collapsed')

    transitions_list = display_transition_input(states, alphabets, num_transitions)
    st.divider()

    if st.button("Convert to DFA"):
        
        nfa = create_nfa(states, alphabets, start_state, accept_states, transitions_list)
    
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.subheader('NFA')
                display_graph_info('NFA', nfa)
                st.latex('''\delta (transition \; table) ''')
                st.table(create_transition_table(transitions_list))
                nfa_svg_content = create_graph('NFA', nfa.get_transitions(), nfa.get_initial_state().get_name(), [state.get_name() for state in nfa.get_final_states()])
            st.markdown(get_svg_as_base64(nfa_svg_content), unsafe_allow_html=True)

        with c2:
            converter = AutomataConverter(nfa, minimized=False)
            dfa = converter.convert_to_dfa(minimized=False)
            with st.container(border=True):
                
                st.subheader('DFA')
                display_graph_info('DFA', dfa)
                st.latex('''\delta (transition \; table) ''')
                                
                transitions = dfa.get_transitions() 
                st.table(create_transition_table(transitions))
                dfa_svg_content = create_graph('DFA', dfa.get_transitions(), dfa.get_initial_state().get_name(), [state.get_name() for state in dfa.get_final_states()])
            st.markdown(get_svg_as_base64(dfa_svg_content), unsafe_allow_html=True)
        with st.expander(" **Minimize DFA**"):
            st.markdown('##### ' + '\n ##### '.join(dfa.minimize()).replace('?', 'Ø'))

if __name__ == "__main__":
    main()