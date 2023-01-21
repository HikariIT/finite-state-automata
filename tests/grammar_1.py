from grammars.earley.algorithm import Earley
from grammars.grammar import Grammar
from grammars.production_list import ProductionList

from languages.alphabet import Alphabet

grammar = Grammar(
    Alphabet({"T", "E", "P"}),
    Alphabet({"+", "*", "a"}),
    "E",
    ProductionList.productions_from_str(
        """E -> T | E+T
        T -> P | T*P
        P -> a
        """
    )
)

print(grammar)
earley = Earley(grammar)
print(earley.word_in_grammar("a+a*a"))
print("\n")

grammar_2 = Grammar(
    Alphabet({"S", "M", "T"}),
    Alphabet({"+", "*", "1", "2", "3", "4"}),
    "S",
    ProductionList.productions_from_str(
        """S -> S+M | M
        M -> M*T | T
        T -> 1 | 2 | 3 | 4
        """
    )
)

print(grammar_2)
earley_2 = Earley(grammar_2)
print(earley_2.word_in_grammar("2+3*4"))