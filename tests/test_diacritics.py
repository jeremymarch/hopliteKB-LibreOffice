# import pytest
import sys
import os
sys.path.append(os.path.abspath("src/py"))

from hopliteaccent import *

def test_diacritics():
    letter = accentLetter("α", DiacriticKey.ACUTE, UnicodeMode.PRECOMPOSED, True)
    assert(letter == "ά")

    letter = accentLetter(letter, DiacriticKey.SMOOTH_BREATHING, UnicodeMode.PRECOMPOSED, True)
    assert(letter == "ἄ")

    letter = accentLetter(letter, DiacriticKey.MACRON, UnicodeMode.PRECOMPOSED, True)
    assert(letter == "α\u0304\u0313\u0301")

    letter = accentLetter(letter, DiacriticKey.IOTA_SUBSCRIPT, UnicodeMode.PRECOMPOSED, True)
    assert(letter == "α\u0304\u0313\u0301\u0345")

    #turn off iota subscript with toggle off == True
    letter = accentLetter(letter, DiacriticKey.IOTA_SUBSCRIPT, UnicodeMode.PRECOMPOSED, True)
    assert(letter == "α\u0304\u0313\u0301")

    #turn on iota subscript in PUA mode
    letter = accentLetter(letter, DiacriticKey.IOTA_SUBSCRIPT, UnicodeMode.PRECOMPOSED_WITH_PUA, True)
    assert(letter == "\ueb07\u0345")

    #toggle off is false: do nothing, if diacritic is present
    letter = accentLetter(letter, DiacriticKey.IOTA_SUBSCRIPT, UnicodeMode.PRECOMPOSED_WITH_PUA, False)
    assert(letter == "\ueb07\u0345")

    #combining mode
    letter = accentLetter("α", DiacriticKey.ACUTE, UnicodeMode.COMBINING_ONLY, True)
    assert(letter == "α\u0301")

    letter = accentLetter(letter, DiacriticKey.ROUGH_BREATHING, UnicodeMode.COMBINING_ONLY, True)
    assert(letter == "α\u0314\u0301")

    letter = accentLetter(letter, DiacriticKey.IOTA_SUBSCRIPT, UnicodeMode.COMBINING_ONLY, True)
    assert(letter == "α\u0314\u0301\u0345")
