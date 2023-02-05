# import pytest
import sys
import os
sys.path.append(os.path.abspath("src/py"))

from hopliteaccent import *


def test_diacritics():
    letter = accentLetter("α", kACUTE, PRECOMPOSED_MODE, True)
    assert(letter == "ά")

    letter = accentLetter(letter, kSMOOTH_BREATHING, PRECOMPOSED_MODE, True)
    assert(letter == "ἄ")

    letter = accentLetter(letter, kMACRON, PRECOMPOSED_MODE, True)
    assert(letter == "α\u0304\u0313\u0301")

    letter = accentLetter(letter, kIOTA_SUBSCRIPT, PRECOMPOSED_MODE, True)
    assert(letter == "α\u0304\u0313\u0301\u0345")

    #turn off iota subscript with toggle off == True
    letter = accentLetter(letter, kIOTA_SUBSCRIPT, PRECOMPOSED_MODE, True)
    assert(letter == "α\u0304\u0313\u0301")

    #turn on iota subscript in PUA mode
    letter = accentLetter(letter, kIOTA_SUBSCRIPT, PRECOMPOSED_WITH_PUA_MODE, True)
    assert(letter == "\ueb07\u0345")

    #toggle off is false: do nothing, if diacritic is present
    letter = accentLetter(letter, kIOTA_SUBSCRIPT, PRECOMPOSED_WITH_PUA_MODE, False)
    assert(letter == "\ueb07\u0345")

    #combining mode
    letter = accentLetter("α", kACUTE, COMBINING_ONLY_MODE, True)
    assert(letter == "α\u0301")

    letter = accentLetter(letter, kROUGH_BREATHING, COMBINING_ONLY_MODE, True)
    assert(letter == "α\u0314\u0301")

    letter = accentLetter(letter, kIOTA_SUBSCRIPT, COMBINING_ONLY_MODE, True)
    assert(letter == "α\u0314\u0301\u0345")
