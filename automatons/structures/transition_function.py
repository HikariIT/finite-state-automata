from __future__ import annotations

from typing import Dict, Set, FrozenSet, List, Tuple

from automatons.exceptions.exceptions import TransitionFunctionError
from automatons.structures.state import State


class TransitionFunction:

    # Set of all automaton states
    states: Set[State]

    # Set of all symbols of automaton
    symbols: FrozenSet[str]

    # Map of all transitions, the function itself
    transition_map: Dict[str, Dict[str, str | Set[str]]]

    # Map of states and their names
    state_map: Dict[str, State]

    def __init__(self, states, symbols):
        self.symbols = symbols
        self.states = states
        self.state_map = {}
        self.transition_map = {}
        for state in states:
            self.transition_map[state] = {}

    def add_state(self, state: State):
        self.state_map[state.name] = state
        self.transition_map[state.name] = {}

    def set_transitions_for_state(self, state: State, targets: List[Set[str]] | List[str]):
        pass


class DeterministicTransitionFunction(TransitionFunction):

    transition_map: Dict[str, Dict[str, str]]

    def __init__(self, states, symbols):
        super().__init__(states, symbols)

    def __call__(self, state: State, symbol: str) -> State:
        if symbol not in self.transition_map[state.name]:
            raise TransitionFunctionError(
                f"DFA Transition function doesn't define transition from state '{state}' with symbol '{symbol}'"
            )
        state_name = self.transition_map[state.name][symbol]
        if state_name not in self.state_map:
            raise KeyError(f"State with name {state_name} is not defined")
        return self.state_map[state_name]

    def set_transition(self, state: State, symbol: str, target: str):
        self.transition_map[state.name][symbol] = target

    def set_transitions_for_state(self, state: State, targets: List[str]):
        for symbol, target in zip(self.symbols, targets):
            self.transition_map[state.name][symbol] = target

    def set_transitions_for_all_states(self, states: List[State], targets: List[List[str]]):
        for state, state_targets in zip(states, targets):
            for symbol, target in zip(self.symbols, state_targets):
                self.transition_map[state.name][symbol] = target

    def get_edges(self) -> List[Tuple[str, str, Dict[str, str]]]:
        edges = []
        for state in self.states:
            for symbol in self.transition_map[state.name]:
                edges.append((state.name, self.transition_map[state.name][symbol], {'s': symbol}))
        return edges

# -----------------------------
# Below code is not updated yet
# TODO: Change to StateMap
# -----------------------------


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
                raise KeyError(f"State with name {state_name} is not defined")
        return set(self.state_map[name] for name in state_names)

    def set_transition(self, state: State, symbol: str, target: Set[str]):
        self.transition_map[state.name][symbol] = target

    def set_transitions_for_state(self, state: State, targets: List[Set[str]]):
        for symbol, target in zip(self.symbols, targets):
            self.transition_map[state.name][symbol] = target

    def set_transitions_for_all_states(self, states: List[State], targets: List[List[Set[str]]]):
        for state, state_targets in zip(states, targets):
            for symbol, target in zip(self.symbols, state_targets):
                self.transition_map[state.name][symbol] = target


class NonDeterministicEpsilonTransitionFunction(TransitionFunction):

    state_map: Dict[State, Dict[str, Set[State]]]
