from typing import Set


class Alphabet:

    symbols: Set[str]

    def __init__(self, symbols: Set[str]):
        self.symbols = symbols
