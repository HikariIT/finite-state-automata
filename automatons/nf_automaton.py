from __future__ import annotations

import itertools
import math

from typing import Set, List

from automatons.automaton import Automaton
from automatons.df_automaton import DFA
from automatons.exceptions.exceptions import InvalidStateError, InvalidSymbolError
from automatons.structures.state import State
from automatons.structures.transition_function import NonDeterministicTransitionFunction


class NFA(Automaton):
    transition_function: NonDeterministicTransitionFunction

    def __init__(self, states: Set[State], symbols: List[str], start_state: State = None,
                 accept_states: Set[State] = None):

        super().__init__()

        self.states = states
        self.symbols = symbols
        self.transition_function = NonDeterministicTransitionFunction(self.states, self.symbols)
        self.start_state = start_state
        self.accept_states = set() if accept_states is None else accept_states

    def add_state(self, name: str, transition_targets: List[Set[str]], is_starting: bool = False,
                  is_accepting: bool = False) -> State:
        # Create new state and verify if it's starting
        new_state = State(name, is_starting, is_accepting)
        if new_state.is_starting:
            if self.start_state is not None:
                raise InvalidStateError(f"Automaton can't have more than one start state")
            else:
                self.start_state = new_state

        # Saving states in self.states and adding transitions
        self.states.add(new_state)
        self.transition_function.add_state(new_state)
        self.transition_function.set_transitions_for_state(new_state, transition_targets)
        return new_state

    def get_resulting_states(self, word: str):
        # Word verification
        word = word.strip()
        for symbol in word:
            if symbol not in self.symbols:
                raise InvalidSymbolError(f"Invalid symbol '{symbol}' in word '{word}'")
        if not self.start_state:
            raise InvalidStateError("There is no starting state.")

        current_states = {self.start_state}
        for symbol in word:
            current_states = self.get_next_state(current_states, symbol)

        return current_states

    def get_next_state(self, states: Set[State], symbol: str):
        new_states = set()
        for state in states:
            new_states.update(self.transition_function(state, symbol))
        return new_states

    def accepts_word(self, word: str):
        return any(state.is_accepting for state in self.get_resulting_states(word))

    def get_all_accepted_words(self, max_length: int):
        accepted_words = []
        for length in range(1, max_length + 1):
            for word in map(lambda x: ''.join(x), itertools.product(*[self.symbols for _ in range(length)])):
                if self.accepts_word(word):
                    accepted_words.append(word)
        return accepted_words

    def convert_to_dfa(self, map_states=True) -> DFA:
        dfa = DFA(set(), self.symbols)

        visited = []
        states_to_check = [{self.start_state}]
        transitions = []

        while len(states_to_check) > 0:
            state = states_to_check.pop(0)
            visited.append(state)
            resulting_states = [self.get_next_state(state, symbol) for symbol in self.symbols]
            for resulting_state in resulting_states:
                if resulting_state not in visited:
                    states_to_check.append(resulting_state)

            transitions.append([state, *resulting_states])

        state_map = {str(state): self.get_raw_name(state) for state in visited}
        if map_states:
            state_map = {str(state): f"s{i}" for i, state in enumerate(visited)}
        print(state_map)

        for i, transition in enumerate(transitions):
            dfa.add_state(state_map[str(transition[0])],
                          [state_map[str(target)] for target in transition[1:]],
                          i == 0,
                          any(map(lambda x: x.is_accepting, transition[0])))

        return dfa

    def print(self):
        if len(self.states) == 0:
            raise Exception("Can't print table for empty automaton")

        sorted_states = sorted(list(self.states), key=lambda x: x.name)

        # Calculate max length of state and width of each column
        max_state_length = max(max(len(str(state)) for state in self.states), len("State"))
        pad_left = max_state_length + 2
        symbol_lengths = [
            max(
                max(len(self.get_raw_name(self.transition_function(state, symbol))) for state in self.states) + 1,
                len(symbol) + 1
            )
            for symbol in self.symbols
        ]

        # Create Divider
        divider = "+" + "-" * (pad_left + 1)
        for symbol, length in zip(self.symbols, symbol_lengths):
            divider += "+" + "-" * (length + 1)
        divider += "+"

        # Create Table header with symbols
        header = "| State".ljust(pad_left + 2) + "| "
        for symbol, length in zip(self.symbols, symbol_lengths):
            header += symbol.ljust(length) + "| "

        # Create top title
        top_row = "=" * (len(header) - 1)
        title = " NF Automaton table"
        space = len(header) - len(title) - 2

        if space > 2:
            title = title.rjust(len(title) + math.floor(space / 2) - 1)
            title = title.ljust(len(header) - 3)
            title = "|" + title + "|"
            print(top_row, title, sep="\n")
        else:
            print(title)

        # Start printing header and table
        print(divider, header, divider, sep="\n")

        for state in sorted_states:
            start_add = " " if not state.is_starting else ""
            row_string = '| ' + (start_add + str(state)).ljust(pad_left) + '| '
            for symbol, length in zip(self.symbols, symbol_lengths):
                row_string += self.get_raw_name(self.transition_function(state, symbol)).ljust(length) + '| '
            print(row_string, divider, sep="\n")
        print("")

    def get_raw_name(self, states: Set[State]) -> str:
        if len(states) == 0:
            return "Ø"
        ret = "{"
        for state in states:
            ret += state.name + ", "
        ret = ret[:-2]
        return ret + "}"
