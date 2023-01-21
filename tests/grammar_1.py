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
print(earley.word_in_grammar("a*a+a"))
