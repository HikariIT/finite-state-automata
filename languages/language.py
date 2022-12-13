import itertools as it
from languages.alphabet import Alphabet


class Language:

    alphabet: Alphabet

    def __init__(self, alphabet: Alphabet):
        self.alphabet = alphabet

    def __pow__(self, power, modulo=None):
        if power != int(power):
            raise Exception("Non-integer powers not accepted")
        if power < 0:
            raise Exception("Invalid power")

        words = set(''.join(symbol_list) for symbol_list in it.product(*[self.alphabet.symbols for _ in range(int(power))]))
        return Language(Alphabet(words))

    def __mul__(self, other):
        if not isinstance(other, Language):
            raise Exception("Multiplication not defined for non-languages")
        return Language(Alphabet(set(''.join(symbol_list) for symbol_list in it.product(self.alphabet.symbols, other.alphabet.symbols))))

    def __str__(self):
        return "{" + ', '.join(sorted(list(self.alphabet.symbols), key=lambda x: len(x))) + "}"
