from __future__ import annotations

from grammars.production_list import ProductionList, ProductionRule
from languages.alphabet import Alphabet


class Grammar:

    non_terminal: Alphabet
    terminal: Alphabet
    start_symbol: str
    productions: ProductionList

    def __init__(self, non_terminal: Alphabet, terminal: Alphabet, start_symbol: str, productions: ProductionList):
        self.non_terminal = non_terminal
        self.terminal = terminal
        self.start_symbol = start_symbol
        self.productions = productions

    def fix_starting_state(self):
        new_start = self.start_symbol + "'"

        self.productions.add_productions(ProductionRule.from_str(f"{new_start}->{self.start_symbol}"))
        self.non_terminal.add(new_start)
        self.start_symbol = new_start

    def __repr__(self):
        ret = ""

        dashes = max(len(repr(self.productions)) + 2, 30 + len(repr(self.terminal)) + 2)

        ret += "+" + "-" * dashes + "+\n"
        ret += ("| Grammar").ljust(dashes + 1) + "|\n"
        ret += "+" + "-" * dashes + "+\n"
        ret += ("| Non-terminal symbols: ".ljust(30) + repr(self.non_terminal)).ljust(dashes + 1) + "|\n"
        ret += ("| Terminal symbols: ".ljust(30) + repr(self.terminal)).ljust(dashes + 1) + "|\n"
        ret += ("| Starting symbol: ".ljust(30) + self.start_symbol).ljust(dashes + 1) + "|\n"
        ret += "+" + "-" * dashes + "+\n"
        ret += "| Productions".ljust(dashes + 1) + "|\n"
        ret += ("| " + repr(self.productions)).ljust(dashes + 1) + "|\n"
        ret += "+" + "-" * dashes + "+\n"

        return ret

    def is_non_terminal(self, s: str):
        return s in self.non_terminal.symbols

    def is_terminal(self, s: str):
        return s in self.terminal.symbols
