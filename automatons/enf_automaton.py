from __future__ import annotations

from typing import Set, List, Dict

from automatons.df_automaton import DFA
from automatons.exceptions.exceptions import InvalidSymbolError, ClosureError
from automatons.nf_automaton import NFA
from automatons.structures.state import State


class ENFA(NFA):
    """
    Class to represent Non-deterministic Finite Automaton (e-NFA) with epsilon-moves
    """

    e_closure: Dict[State, Set[State]] | None

    """
    Attributes:
        states (Set[State]): 
            Finite set of automaton states
        symbols (List[str]): 
            Finite set of input symbols
        transition_function (NonDeterministicTransitionFunction): 
            Function containing all transitions from one state to others using given symbol
        start_state (State | None): 
            Starting state of the automaton
        accept_states (Set[State]): 
            Set of states which are accepted by the automaton
        null_state (State):
            State which represents empty set
        e_closure (Dict[State, Set[State]] | None
            Dictionary in which keys are States and values are all States achievable from that state with epsilon-move
    """

    def __init__(self, symbols: List[str]):
        """
        Non-deterministic Finite Automaton with epsilon-moves (e-NFA) constructor

        Symbol list must not contain the 'e' symbol, which is reserved for epsilon-moves

        Args:
            symbols (List[str]):
                List of all symbols used by the automaton

        Raises:
            InvalidSymbolError:
                If symbol list contains 'e' symbol
        """
        if "e" in symbols:
            raise InvalidSymbolError("Symbol 'e' is reserved for epsilon-moves")
        symbols.append("e")
        self.e_closure = None
        super().__init__(symbols)

    def add_state(self, name: str, transition_targets: List[Set[str]], is_starting: bool = False,
                  is_accepting: bool = False) -> State:
        """
        Adds a new state to the automaton

        Transition targets must be given in the same order as symbols in the language. For example,
        if symbols are ['0', '1'], then the first element of the list must be the target of transition '0'.

        For e-NFA, last transition is reserved for epsilon symbol.

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
        state = super().add_state(name, transition_targets, is_starting, is_accepting)
        try:
            self._calculate_e_closure()
        except:
            self.e_closure = None

        return state

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
        current_states = self._apply_closure({self.start_state})
        for symbol in word:
            current_states = self.get_next_state(current_states, symbol)
            current_states = self._apply_closure(current_states)

        return current_states

    def convert_to_nfa(self) -> NFA:
        nfa_symbols = list(self.symbols)
        nfa_symbols.pop(-1)
        nfa = NFA(nfa_symbols)
        for state in self.states:
            if state == self.null_state:
                continue
            closure = self.e_closure[state]
            transition_targets = []
            for symbol in nfa_symbols:
                targets = set()
                for closure_state in closure:
                    targets.update(self.transition_function(closure_state, symbol))
                transition_targets.append(self._apply_closure(targets))
            nfa.add_state(state.name, [set(map(lambda x: x.name, target)) for target in transition_targets],
                          state.is_starting, self._is_accepting(state))

        return nfa

    def convert_to_dfa(self, map_states: bool = True) -> DFA:
        nfa = self.convert_to_nfa()
        return nfa.convert_to_dfa(map_states)

    def _calculate_e_closure(self):
        self.e_closure = {}
        for state in self.states:
            self._calculate_e_closure_for_state(state)

    def _calculate_e_closure_for_state(self, state: State) -> Set[State]:
        if state in self.e_closure:
            return self.e_closure[state]

        e_targets = self.transition_function(state, "e")
        closure = {state}
        for target in e_targets:
            closure.update(self._calculate_e_closure_for_state(target))
        self.e_closure[state] = closure
        return self.e_closure[state]

    def _apply_closure(self, states: Set[State]) -> Set[State]:
        result = set()
        for state in states:
            result.update(self.e_closure[state])
        return result

    def _is_accepting(self, state: State) -> bool:
        return any(map(lambda x: x.is_accepting, self.e_closure[state]))

    def print(self, title: str = "e-NF Automaton table"):
        super().print("e-NF Automaton table")