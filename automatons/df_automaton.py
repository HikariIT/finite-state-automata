import math

from typing import List

from automatons.abstract_automaton import AbstractAutomaton
from automatons.structures.state import State
from automatons.structures.transition_function import DeterministicTransitionFunction


class DFA(AbstractAutomaton):

    transition_function: DeterministicTransitionFunction

    def __init__(self, symbols: List[str]):

        super().__init__(symbols)
        self.transition_function = DeterministicTransitionFunction(self.states, self.symbols)

    def add_state(self, name: str, transition_targets: List[str], is_starting: bool = False,
                  is_accepting: bool = False) -> State:
        """
        Adds a new state to the automaton

        Transition targets must be given in the same order as symbols in the language. For example,
        if symbols are ['0', '1'], then the first element of the list must be the target of transition '0'.

        Args:
            name (str):
                State name
            transition_targets (List[str]]):
                List of sets of states achieved from this state with each symbol
            is_starting (bool, optional):
                Sets the state as starting, defaults to False
            is_accepting (bool, optional):
                Sets the state as accepting, defaults to False

        Returns:
            New state created by this method

        Raises:
            InvalidStateError: If there is already a starting state in the Automaton
        """
        return super().add_state(name, transition_targets, is_starting, is_accepting)

    def get_resulting_state(self, word: str) -> State:
        """
        Get state in which automaton finishes its run after given input

        Args:
            word (str):
                Word built with symbols accepted by the automaton

        Returns:
            State in which the automaton finishes its run after given input

        Raises:
            InvalidStateError:
                If there is no starting state
            InvalidSymbolError:
                If the automaton encounters a symbol not present in states attribute
        """
        super().verify_word(word)
        current_state = self.start_state
        for symbol in word:
            current_state = self.transition_function(current_state, symbol)

        return current_state

    def print(self):
        """
        Prints table representation of the automaton
        """
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
