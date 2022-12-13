from languages.alphabet import Alphabet
from languages.language import Language
from regex.regex import Regex

L = Alphabet({"0", "10", "111", "001"})
M = Alphabet({"", "1", "01", "10"})

l_lang = Language(L)
m_lang = Language(M)
print(l_lang ** 2 * m_lang ** 2)

r = Regex()
r.to_postfix("aa*")
