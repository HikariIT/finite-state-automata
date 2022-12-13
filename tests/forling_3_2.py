from automatons.nf_automaton import NFA


# ---------------------------------------------------------------------
# Task 1

nfa = NFA(["0", "1"])
nfa.add_state("q_1",[{"q_1"}, {"q_1", "q_2"}], is_starting=True)
nfa.add_state("q_2",[{"q_3"}, {"q_3"}])
nfa.add_state("q_3",[{"q_4"}, {"q_4"}])
nfa.add_state("q_4",[set(), set()], is_accepting=True)

print(nfa.get_all_accepted_words(5))

# a) Language of words in which "1" is at the 3rd place from the end
# b)

dfa = nfa.convert_to_dfa(map_states=False)
dfa.print()

# ---------------------------------------------------------------------
# Task 2

nfa_2 = NFA(["0", "1"])
nfa_2.add_state("q_1", [{"q_1"}, {"q_1", "q_2"}], is_starting=True)
nfa_2.add_state("q_2", [{"q_3"}, set()])
nfa_2.add_state("q_3", [set(), set()], is_accepting=True)

print(nfa_2.get_all_accepted_words(5))

# a) Language of all words that end in "10"
# b)

dfa_2 = nfa_2.convert_to_dfa(map_states=False)
dfa_2.print()

# ---------------------------------------------------------------------
# Task 3

nfa_3 = NFA(["0", "1"])
nfa_3.add_state("q_1", [{"q_1"}, {"q_1", "q_2"}], is_starting=True)
nfa_3.add_state("q_2", [{"q_3", "q_4"}, {"q_3"}])
nfa_3.add_state("q_3", [set(), {"q_4"}])
nfa_3.add_state("q_4", [{"q_1"}, {"q_2"}], is_accepting=True)

print(nfa_3.get_all_accepted_words(5))

# a)
dfa_3 = nfa_3.convert_to_dfa(map_states=False)
dfa_3.print()





