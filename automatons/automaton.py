from __future__ import annotations

from typing import Set, FrozenSet, List, Dict

from automatons.structures.state import State
from automatons.structures.transition_function import TransitionFunction


class Automaton:

    # Q - finite set of automaton states
    states: Set[State]

    # Sigma - finite set of input symbols
    symbols: List[str]

    # Delta - transition function
    transition_function: TransitionFunction

    # Q_0 - starting state
    start_state: State | None

    # F - accept states
    accept_states: Set[State]

    def __init__(self):
        self.states = set()
        self.symbols = []
        self.start_state = None
        self.accept_states = set()