from typing import Set


class Alphabet:

    symbols: Set[str]

    def __init__(self, symbols: Set[str]):
        self.symbols = symbols

    def add(self, symbol: str):
        self.symbols.add(symbol)

    def __repr__(self):
        return ", ".join(self.symbols)