import math

from typing import List, FrozenSet, Set

from automatons.abstract_automaton import AbstractAutomaton
from automatons.structures.state import State
from automatons.structures.transition_function import DeterministicTransitionFunction


class DFA(AbstractAutomaton):
    """
    Class to represent Deterministic Finite Automaton (DFA)
    """

    transition_function: DeterministicTransitionFunction

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
    """

    def __init__(self, symbols: List[str]):
        """
        Deterministic Finite Automaton (DFA) constructor

        Args:
            symbols (List[str]):
                List of all symbols used by the automaton
        """
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
        symbol_lengths = [
            max(
                max(len(state.name) for state in self.states) + 1,
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

    def minimize(self):
        self._remove_unreachable_states()
        non_distinguishable = self._hopcroft_non_distinguishable()
        for i, equivalence_class in enumerate(filter(lambda x: len(x) > 1, non_distinguishable)):
            self._merge_states(i + 1, equivalence_class)
        pass

    def _remove_unreachable_states(self):

        # Code adapted from https://en.wikipedia.org/wiki/DFA_minimization
        reachable_states = {self.start_state}
        new_states = {self.start_state}
        while True:
            temp = set()
            for state in new_states:
                for symbol in self.symbols:
                    temp.add(self.transition_function(state, symbol))
            new_states = temp.difference(reachable_states)
            reachable_states.update(new_states)
            if len(new_states) == 0:
                break
        unreachable_states = self.states.difference(reachable_states)
        for state in unreachable_states:
            self.remove_state(state)
        if len(unreachable_states) > 0:
            print(f"Removing unreachable states: {unreachable_states} ...")
        else:
            print(f"No unreachable states found...")

    def _hopcroft_non_distinguishable(self) -> Set[FrozenSet[State]]:

        # Code adapted from https://en.wikipedia.org/wiki/DFA_minimization
        p: Set[FrozenSet[State]] = {frozenset({self.start_state}),
                                    frozenset(self.states.difference({self.start_state}))}
        w: Set[FrozenSet[State]] = {frozenset({self.start_state}),
                                    frozenset(self.states.difference({self.start_state}))}

        self.print()

        while len(w) > 0:
            a = w.pop()
            for symbol in self.symbols:
                x = frozenset(state for state in self.states if self.transition_function(state, symbol) in a)

                add_to_p: Set[FrozenSet[State]] = set()
                add_to_w: Set[FrozenSet[State]] = set()

                remove_from_p: Set[FrozenSet[State]] = set()
                remove_from_w: Set[FrozenSet[State]] = set()

                for y in p:
                    inter = frozenset(x.intersection(y))
                    diff = frozenset(y.difference(x))

                    if len(inter) > 0 and len(diff) > 0:

                        remove_from_p.add(y)
                        add_to_p.add(inter)
                        add_to_p.add(diff)

                        if y in w:
                            remove_from_w.add(y)
                            add_to_w.add(inter)
                            add_to_w.add(diff)

                        else:
                            if len(inter) <= len(diff):
                                add_to_w.add(inter)
                            else:
                                add_to_w.add(diff)

                p.difference_update(remove_from_p)
                p.update(add_to_p)

                w.difference_update(remove_from_w)
                w.update(add_to_w)

        return p

    def _merge_states(self, index: int, states: FrozenSet[State]):

        state_name = f"r{index}"

        # Create transitions
        state = list(states)[0]
        transition_targets = [self.transition_function(state, symbol) for symbol in self.symbols]
        fixed_targets = []
        for target in transition_targets:
            if target in states:
                fixed_targets.append(state_name)

        # Remove states
        for state in states:
            self.remove_state(state)

        # Change all transitions leading to merged states
        for symbol in self.symbols:
            for state in self.states:
                transition_result = self.transition_function(state, symbol)
                if not transition_result:
                    self.transition_function.set_transition(state, symbol, state_name)

        merged_state = self.add_state(state_name,
                                      fixed_targets,
                                      any(map(lambda x: x.is_starting, states)),
                                      any(map(lambda x: x.is_accepting, states))
                                      )

