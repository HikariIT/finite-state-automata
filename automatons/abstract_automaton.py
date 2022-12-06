from __future__ import annotations

import itertools
from typing import Set, List
from abc import ABC, abstractmethod

from automatons.exceptions.exceptions import InvalidStateError, InvalidSymbolError
from automatons.structures.state import State
from automatons.structures.transition_function import TransitionFunction


class AbstractAutomaton(ABC):
    """
    Abstract class to represent Finite State Automatons
    """

    states: Set[State]
    symbols: List[str]
    transition_function: TransitionFunction
    start_state: State | None
    accept_states: Set[State]

    """
    Attributes:
        states (Set[State]): Finite set of automaton states
        symbols (List[str]): Finite set of input symbols
        transition_function (NonDeterministicTransitionFunction): Function containing all transitions from one state 
            to others using given symbol
        start_state (State | None): Starting state of the automaton
        accept_states (Set[State]): Set of states which are accepted by the automaton
    """

    def __init__(self, symbols: List[str]):
        self.states = set()
        self.symbols = symbols
        self.start_state = None
        self.accept_states = set()

    def add_state(self, name: str, transition_targets: List[Set[str]] | List[str],
                  is_starting: bool = False, is_accepting: bool = False) -> State:

        new_state = State(name, is_starting, is_accepting)

        # Verify if there is no more than one starting state
        if new_state.is_starting:
            if self.start_state is not None:
                raise InvalidStateError(f"Automaton can't have more than one start state")
            else:
                self.start_state = new_state

        self.states.add(new_state)
        self.transition_function.add_state(new_state)
        self.transition_function.set_transitions_for_state(new_state, transition_targets)
        return new_state

    def accepts_word(self, word: str):
        """
        Verifies if the automaton accepts a given word

        Args:
            word (str):
                Word built with symbols accepted by the automaton

        Returns:
            True if automaton finishes in an accepting state, False otherwise

        """
        return self.get_resulting_state(word).is_accepting

    def verify_word(self, word: str):
        """
        Verifies if the word is valid

        Args:
            word (str):
                Word built with symbols accepted by the automaton

        Returns:
            True if word is valid, False otherwise
        """
        word = word.strip()
        for symbol in word:
            if symbol not in self.symbols:
                raise InvalidSymbolError(f"Invalid symbol '{symbol}' in word '{word}'")
        if not self.start_state:
            raise InvalidStateError("There is no starting state")

    def get_all_accepted_words(self, max_length: int) -> List[str]:
        """
        Get all words of length up to a given number which are accepted by the automaton

        Args:
            max_length (int):
                Max length of word

        Returns:
            List of words
        """
        accepted_words = []
        for length in range(1, max_length + 1):
            for word in map(lambda x: ''.join(x), itertools.product(*[self.symbols for _ in range(length)])):
                if self.accepts_word(word):
                    accepted_words.append(word)
        return accepted_words

    @abstractmethod
    def get_resulting_state(self, word: str) -> Set[State] | State:
        pass

    @abstractmethod
    def print(self):
        pass