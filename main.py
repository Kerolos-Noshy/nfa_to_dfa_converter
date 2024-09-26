import pandas as pd
import streamlit as st
from graph_creator import create_graph
from automata.nfa import NFA
from automata.automata_converter import AutomataConverter
from automata.state import State


def create_transition_table(transitions):
    states = set()
    symbols = set()

    for from_state, symbol, to_state in transitions:
        states.add(from_state)
        states.add(to_state)
        if symbol == 'e':
            symbols.update('ε')
        else:
            symbols.update(symbol)

    symbols = sorted(symbols)

    state_list = sorted(map(str, states))

    transition_dict = {state: {symbol: list() for symbol in symbols} for state in state_list}

    for from_state, symbol, to_state in transitions:
        transition_dict[str(from_state)][symbol.replace('e', 'ε')].append(str(to_state))

    df = pd.DataFrame(columns=symbols)

    for state, symbol_dict in transition_dict.items():
        for symbol, to_states in symbol_dict.items():
            # Convert set of states to a sorted list of strings
            df.at[state, symbol] = ', '.join(sorted(to_states)) if to_states else '∅'
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'State'}, inplace=True)
    return df



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


def display_graph_info(automata):
    col1, col2 = st.columns(2)
    with col1:
        states = sorted([state.get_name() for state in automata.get_states()])
        st.latex('''Q (states) =  \{ ''' + ', '.join(states) + ''' \}''')
        st.latex('''q_0 (initial \; state) =  \{ ''' + automata.get_initial_state().get_name() + ''' \}''')
    with col2:
        st.latex('''E (alphabets) =  \{ ''' + ', '.join(sorted(automata.get_alphabets())).replace('e', 'ε') + ''' \}''')
        st.latex('''F (accepting \; states) =  \{ ''' + ', '.join([accept_state.get_name() for accept_state in automata.get_final_states()]) + ''' \}''')


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


def convert_to_dfa(states, alphabets, start_state, accept_states, transitions_list):
    nfa = create_nfa(states, alphabets, start_state, accept_states, transitions_list)

    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.subheader('NFA')
            display_graph_info(nfa)
            st.latex('''\delta (transition \; table) ''')
            st.table(create_transition_table(transitions_list))
            nfa_fig = create_graph('NFA', nfa)
        # st.markdown(get_svg_as_base64(nfa_svg_content), unsafe_allow_html=True)

    with c2:
        converter = AutomataConverter(nfa)
        dfa = converter.convert_to_dfa()
        with st.container(border=True):
            st.subheader('DFA')
            display_graph_info(dfa)
            st.latex('''\delta (transition \; table) ''')

            transitions = dfa.get_transitions()
            st.table(create_transition_table(transitions))
            dfa_fig = create_graph('DFA', dfa)

        # st.markdown(get_svg_as_base64(dfa_svg_content), unsafe_allow_html=True)
    with st.container():
        st.info("""**Green color for the start state**
                \n **Red color for the final states** """, icon='ℹ️')

        co1, co2 = st.columns(2)
        with co1:
            st.pyplot(nfa_fig)

        with co2:
            st.pyplot(dfa_fig)
        st.markdown("Graphs are not clear? Click on `Convert to DFA` Again")

    with st.container(border=True):
        st.subheader('Minimized DFA')
        last_equivalence = dfa.minimize()[-1]
        minimized_dfa = dfa.convert_minimization_to_DFA(last_equivalence)
        minimized_dfa_fig = create_graph('Minimized DFA', minimized_dfa)

        minimized_transitions = minimized_dfa.get_transitions()
        col1, col2 = st.columns(2)
        with col1:
            display_graph_info(nfa)
            st.latex('''\delta (transition \; table) ''')
            st.table(create_transition_table(minimized_transitions))
        with col2:
            st.pyplot(minimized_dfa_fig)
        st.markdown('##### ' + '\n ##### '.join(dfa.print_minimization()))


def main():
    st.set_page_config(page_title="NFA to DFA Converter", layout="wide", initial_sidebar_state="auto")
    st.title("NFA to DFA Converter")
    st.header("Input your NFA details")

    num_transitions = st.sidebar.number_input("Number of transitions", min_value=1, value=3)
    states, alphabets = display_states_and_alphabets()
    st.markdown("##### Enter the start state:")
    start_state = st.selectbox("Enter the start state:", states, label_visibility='collapsed')


    # accept_states = st.text_input("Enter the accept states (comma-separated):", "q2")
    st.markdown("##### Enter the accept states (multiselect):")
    accept_states = st.multiselect("Enter the accept states (multiselect):", states, label_visibility='collapsed')

    transitions_list = display_transition_input(states, alphabets, num_transitions)
    st.divider()

    if st.button("Convert to DFA"):
        convert_to_dfa(states, alphabets, start_state, accept_states, transitions_list)


if __name__ == "__main__":
    main()