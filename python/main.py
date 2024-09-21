import pandas as pd
import streamlit as st
from dfa_text_handler import handle_dfa
from script import get_dfa_output
from graph_creator import create_graph
import utils
from nfa_text_handler import (
    get_transitions,
    get_initial_state,
    get_accepting_states,
    get_alphabets,
    get_states
)

def get_transitions_table(transitions):
    df = pd.DataFrame(transitions).T
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'State'}, inplace=True)
    df.fillna('', inplace=True)
    return df.rename({'e': "ε"}, axis=1)

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

def display_graph_info(graph_type, lines):
    col1, col2 = st.columns(2)
    with col1:
        st.latex('''Q (states) =  \{ ''' + ', '.join(get_states(lines)).replace('?', 'Ø') + ''' \}''')
        st.latex('''q_0 (initial \; state) =  \{ ''' + get_initial_state(lines) + ''' \}''')
    with col2:
        st.latex('''E (alphabets) =  \{ ''' + ', '.join(get_alphabets(lines)) + ''' \}''')
        st.latex('''F (accepting \; states) =  \{ ''' + ', '.join(get_accepting_states(lines)) + ''' \}''')

def save_nfa_to_file(states, alphabets, start_state, accept_states, transitions_list):
    with open(f'{utils.OUTPUT_FOLDER}/nfa.txt', 'w', encoding="utf-8") as f:
        f.write(f"{','.join(states)}\n{','.join(alphabets)}\n{start_state}\n{','.join(accept_states)}\n")
        f.write("".join(f"{s1}, {a}, {s2}\n" for s1, a, s2 in transitions_list))


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
        save_nfa_to_file(states, alphabets, start_state, accept_states, transitions_list)
        get_dfa_output()
        handle_dfa()

        with open(f'{utils.OUTPUT_FOLDER}/nfa.txt', 'r') as f:
            nfa_lines = f.readlines()

        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.subheader('NFA')
                display_graph_info('NFA', nfa_lines)
                st.latex('''\delta (transition \; table) ''')
                st.table(get_transitions_table(get_transitions(nfa_lines)))
                create_graph('NFA', get_transitions(nfa_lines), get_initial_state(nfa_lines), get_accepting_states(nfa_lines))
            st.markdown(utils.get_svg_as_base64(f'{utils.OUTPUT_FOLDER}/NFA_graph.svg'), unsafe_allow_html=True)

        with c2:
            with st.container(border=True):
                with open(f'{utils.OUTPUT_FOLDER}/dfa_formated.txt', 'r') as f:
                    dfa_lines = f.readlines()
                st.subheader('DFA')
                display_graph_info('DFA', dfa_lines)
                st.latex('''\delta (transition \; table) ''')
                st.table(get_transitions_table(get_transitions(dfa_lines)).replace('?', 'Ø'))
                create_graph('DFA', get_transitions(dfa_lines), get_initial_state(dfa_lines), get_accepting_states(dfa_lines))
            st.markdown(utils.get_svg_as_base64(f'{utils.OUTPUT_FOLDER}/DFA_graph.svg'), unsafe_allow_html=True)

        with st.expander(" **Minimize DFA**"):
            with open(f'{utils.OUTPUT_FOLDER}/minimized_dfa.txt', 'r') as f:
                minimized_lines = f.readlines()
            st.markdown('##### ' + '\n ##### '.join(minimized_lines).replace('?', 'Ø'))

if __name__ == "__main__":
    main()