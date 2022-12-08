from __future__ import annotations

import math

from typing import Set, List

from automatons.df_automaton import DFA
from automatons.exceptions.exceptions import InvalidSymbolError
from automatons.structures.state import State
from automatons.abstract_automaton import AbstractAutomaton
from automatons.structures.transition_function import NonDeterministicTransitionFunction


class NFA(AbstractAutomaton):
    """
    Class to represent Non-deterministic Finite Automaton (NFA) without ϵ-moves
    """

    transition_function: NonDeterministicTransitionFunction
    null_state: State

    """
    Attributes:
        states (Set[State]): 
            Finite set of automaton states
        symbols (List[str]): 
            List of input symbols
        transition_function (NonDeterministicTransitionFunction): 
            Function containing all transitions from one state to others using given symbol
        start_state (State | None): 
            Starting state of the automaton
        accept_states (Set[State]): 
            Set of states which are accepted by the automaton
        null_state (State):
            State which represents empty set
    """

    def __init__(self, symbols: List[str]):
        """
        Non-deterministic Finite Automaton (NFA) constructor

        Args:
            symbols (List[str]):
                List of all symbols used by the automaton
        """
        super().__init__(symbols)
        self.transition_function = NonDeterministicTransitionFunction(self.states, self.symbols)
        self.null_state = self.add_state("Ø", [set() for _ in self.symbols])

    def add_state(self, name: str, transition_targets: List[Set[str]], is_starting: bool = False,
                  is_accepting: bool = False) -> State:
        """
        Adds a new state to the automaton

        Transition targets must be given in the same order as symbols in the language. For example,
        if symbols are ['0', '1'], then the first element of the list must be the target of transition '0'.

        Args:
            name (str):
                State name
            transition_targets (List[Set[str]]):
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

    def get_resulting_state(self, word: str) -> Set[State]:
        """
        Get states in which automaton finishes its run after given input

        Args:
            word (str):
                Word built with symbols accepted by the automaton

        Returns:
            Set of states in which the automaton finishes its run after given input

        Raises:
            InvalidStateError:
                If there is no starting state
            InvalidSymbolError:
                If the automaton encounters a symbol not present in states attribute
        """
        self.verify_word(word)
        current_states = {self.start_state}
        for symbol in word:
            current_states = self.get_next_state(current_states, symbol)

        return current_states

    def get_next_state(self, states: Set[State], symbol: str) -> Set[State]:
        """
        Get set of states to which automaton transitions from given set of states after a single-symbol input

        Args:
            states (Set[State]):
                States from which the automaton transitions
            symbol (str):
                Symbol input

        Returns:
            Set of states to which automaton transitions after the input

        Raises:
            InvalidSymbolError:
                If the automaton encounters a symbol not present in states attribute
        """
        if symbol not in self.symbols:
            raise InvalidSymbolError(f"Invalid symbol '{symbol}'")
        new_states = set()
        for state in states:
            new_states.update(self.transition_function(state, symbol))
        return new_states

    def accepts_word(self, word: str):
        return any(state.is_accepting for state in self.get_resulting_state(word))

    def convert_to_dfa(self, map_states: bool = True) -> DFA:
        """
        Converts NFA to DFA

        Args:
            map_states (bool):
                If True, state names in DFA are replaced with convention s_{i}, where i is an integer starting from 0.
                If False, state names are left unchanged.

        Returns:
            Resulting DFA
        """
        dfa = DFA(self.symbols)

        visited = []
        states_to_check = [{self.start_state}]
        transitions = []

        while len(states_to_check) > 0:
            state = states_to_check.pop(0)
            if state in visited:
                continue
            visited.append(state)
            resulting_states = [self.get_next_state(state, symbol) for symbol in self.symbols]
            for resulting_state in resulting_states:
                if resulting_state not in visited:
                    states_to_check.append(resulting_state)

            transitions.append([state, *resulting_states])

        state_map = {tuple(sorted(state, key=lambda x: x.name)): self._get_raw_name(state) for state in visited}
        if map_states:
            state_map = {tuple(sorted(state, key=lambda x: x.name)): f"s{i}" for i, state in enumerate(visited)}

        for i, transition in enumerate(transitions):
            dfa.add_state(state_map[tuple(sorted(transition[0], key=lambda x: x.name))],
                          [state_map[tuple(sorted(target, key=lambda x: x.name))] for target in transition[1:]],
                          i == 0,
                          any(map(lambda x: x.is_accepting, transition[0])))

        return dfa

    def print(self, title: str = "NF Automaton table"):
        """
        Prints table representation of the automaton
        """
        if len(self.states) == 0:
            raise Exception("Can't print table for empty automaton")

        states = list(self.states)
        states.remove(self.null_state)
        sorted_states = sorted(states, key=lambda x: x.name)

        # Calculate max length of state and width of each column
        max_state_length = max(max(len(str(state)) for state in self.states), len("State"))
        pad_left = max_state_length + 2
        symbol_lengths = [
            max(
                max(len(self._get_raw_name(self.transition_function(state, symbol))) for state in self.states) + 1,
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
                row_string += self._get_raw_name(self.transition_function(state, symbol)).ljust(length) + '| '
            print(row_string, divider, sep="\n")
        print("")

    @staticmethod
    def _get_raw_name(states: Set[State]) -> str:
        """
        Returns string representation of State set, in which States are referred to only by their names
        (There are no * or > in raw name)

        Args:
            states (Set[State]):
                Set of states to be represented

        Returns:
            Raw string representation of the set
        """
        if len(states) == 0:
            return "Ø"
        ret = "{"
        for state in states:
            ret += state.name + ", "
        ret = ret[:-2]
        return ret + "}"
