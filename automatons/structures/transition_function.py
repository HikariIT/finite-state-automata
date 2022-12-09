from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Set, List

from automatons.exceptions.exceptions import TransitionFunctionError, InvalidStateError
from automatons.structures.state import State


class TransitionFunction(ABC):
    """
    Abstract class representing a transition function
    """

    states: Set[State]
    symbols: List[str]
    transition_map: Dict[str, Dict[str, str | Set[str]]]
    state_map: Dict[str, State]

    """
    Attributes:
        states (Set[State]): 
            Finite set of automaton states
        symbols (List[str]): 
            List of input symbols
        transition_map (Dict[str, Dict[str, str | Set[str]]]): 
            Dictionary of transitions in which keys are state names and values are dictionaries of symbol 
            and their respective targets
        state_map (Dict[str, State])
            Dictionary of state names and their instances
    """

    def __init__(self, states: Set[State], symbols: List[str]):
        """
        Constructor of abstract transition function

        Args:
            states (Set[State]):
                Finite set of automaton states
            symbols (List[str]):
                List of input symbols
        """
        self.symbols = symbols
        self.states = states
        self.state_map = {}
        self.transition_map = {}
        for state in states:
            self.transition_map[state.name] = {}

    def add_state(self, state: State):
        """
        Adds a new state to transition function

        Args:
            state (State):
                State to add
        """
        self.state_map[state.name] = state
        self.transition_map[state.name] = {}

    def remove_state(self, state: State):
        self.state_map.pop(state.name)
        self.transition_map.pop(state.name)

    @abstractmethod
    def set_transitions_for_state(self, state: State, targets: List[Set[str]] | List[str]):
        pass

# TODO: Add comments to Transition functions (deterministic and non-deterministic)


class DeterministicTransitionFunction(TransitionFunction):

    transition_map: Dict[str, Dict[str, str]]

    def __init__(self, states, symbols):
        super().__init__(states, symbols)

    def __call__(self, state: State, symbol: str) -> State | None:
        if symbol not in self.transition_map[state.name]:
            raise TransitionFunctionError(
                f"DFA Transition function doesn't define transition from state '{state}' with symbol '{symbol}'"
            )
        state_name = self.transition_map[state.name][symbol]
        if state_name not in self.state_map:
            return None
            # raise KeyError(f"State with name {state_name} is not defined")
        return self.state_map[state_name]

    def set_transition(self, state: State, symbol: str, target: str):
        self.transition_map[state.name][symbol] = target

    def set_transitions_for_state(self, state: State, targets: List[str]):
        for symbol, target in zip(self.symbols, targets):
            self.transition_map[state.name][symbol] = target


class NonDeterministicTransitionFunction(TransitionFunction):

    transition_map: Dict[str, Dict[str, Set[str]]]

    def __init__(self, states, symbols):
        super().__init__(states, symbols)

    def __call__(self, state: State, symbol: str) -> Set[State]:
        # If there is no transition, return an empty set
        if symbol not in self.transition_map[state.name]:
            return set()
        state_names = self.transition_map[state.name][symbol]
        for state_name in state_names:
            if state_name not in self.state_map:
                raise InvalidStateError(f"State with name {state_name} is not defined")
        return set(self.state_map[name] for name in state_names)

    def set_transition(self, state: State, symbol: str, target: Set[str]):
        self.transition_map[state.name][symbol] = target

    def set_transitions_for_state(self, state: State, targets: List[Set[str]]):
        for symbol, target in zip(self.symbols, targets):
            self.transition_map[state.name][symbol] = target