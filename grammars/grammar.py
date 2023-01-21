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

        ret += "+-------------------------------------------------------\n"
        ret += "| Grammar\n"
        ret += "+-------------------------------------------------------\n"
        ret += "| Non-terminal symbols: ".ljust(30) + repr(self.non_terminal) + "\n"
        ret += "| Terminal symbols: ".ljust(30) + repr(self.terminal) + "\n"
        ret += "| Starting symbol: ".ljust(30) + self.start_symbol + "\n"
        ret += "+-------------------------------------------------------\n"
        ret += "| Productions\n"
        ret += "| " + repr(self.productions) + "\n"
        ret += "+-------------------------------------------------------\n"

        return ret

    def is_non_terminal(self, s: str):
        return s in self.non_terminal.symbols

    def is_terminal(self, s: str):
        return s in self.terminal.symbols
