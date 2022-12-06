import itertools
import math

import networkx as nx
from networkx.drawing.nx_agraph import write_dot

from typing import Set, List

from automatons.automaton import Automaton
from automatons.exceptions.exceptions import InvalidStateError, InvalidSymbolError
from automatons.structures.state import State
from automatons.structures.transition_function import TransitionFunction, DeterministicTransitionFunction


class DFA(Automaton):

    transition_function: DeterministicTransitionFunction

    def __init__(self, states: Set[State], symbols: List[str], start_state: State = None,
                 accept_states: Set[State] = None):

        super().__init__()

        self.states = states
        self.symbols = symbols
        self.transition_function = DeterministicTransitionFunction(self.states, self.symbols)
        self.start_state = start_state
        self.accept_states = set() if accept_states is None else accept_states

    def add_state(self, name: str, transition_targets: List[str], is_starting: bool = False, is_accepting: bool = False) -> State:

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

    def get_resulting_state(self, word: str):
        # Word verification
        word = word.strip()
        for symbol in word:
            if symbol not in self.symbols:
                raise InvalidSymbolError(f"Invalid symbol '{symbol}' in word '{word}'")

        current_state = self.start_state
        for symbol in word:
            current_state = self.transition_function(current_state, symbol)

        return current_state

    def accepts_word(self, word: str):
        return self.get_resulting_state(word).is_accepting

    def get_all_accepted_words(self, max_length: int):
        accepted_words = []
        for length in range(1, max_length + 1):
            for word in map(lambda x: ''.join(x), itertools.product(*[self.symbols for _ in range(length)])):
                if self.accepts_word(word):
                    accepted_words.append(word)
        return accepted_words

    def print(self):
        if len(self.states) == 0:
            raise Exception("Can't print table for empty automaton")

        sorted_states = sorted(list(self.states), key=lambda x: x.name)

        # Calculate max length of state and width of each column
        max_state_length = max(max(len(str(state)) for state in self.states), len("State"))
        pad_left = max_state_length + 2
        symbol_lengths = [max(pad_left - 2, len(symbol) + 1) for symbol in self.symbols]

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
        title = " DF Automaton table"
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
                row_string += self.transition_function(state, symbol).name.ljust(length) + '| '
            print(row_string, divider, sep="\n")
        print("")
