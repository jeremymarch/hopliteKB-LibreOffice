# hoplite_accent is added to sys.path in pyproject.toml
from hoplite_accent import Diacritic, UnicodeMode, accent_letter


def test_diacritics():
    letter = accent_letter("α", Diacritic.ACUTE, UnicodeMode.PRECOMPOSED, True)
    assert letter == "ά"

    # pass diacritic parameter as int
    letter = accent_letter("α", 5, UnicodeMode.PRECOMPOSED, True)
    assert letter == "ά"

    # pass diacritic parameter as str
    letter = accent_letter("α", "5", UnicodeMode.PRECOMPOSED, True)
    assert letter == "ά"

    # pass diacritic parameter out of range
    letter = accent_letter("α", 1000, UnicodeMode.PRECOMPOSED, True)
    assert letter is None

    letter = accent_letter("ά", Diacritic.SMOOTH_BREATHING, UnicodeMode.PRECOMPOSED, True)
    assert letter == "ἄ"

    letter = accent_letter("ἄ", Diacritic.MACRON, UnicodeMode.PRECOMPOSED, True)
    assert letter == "α\u0304\u0313\u0301"

    letter = accent_letter("α\u0304\u0313\u0301", Diacritic.IOTA_SUBSCRIPT, UnicodeMode.PRECOMPOSED, True)
    assert letter == "α\u0304\u0313\u0301\u0345"

    # turn off iota subscript with toggle_off == True
    letter = accent_letter("α\u0304\u0313\u0301\u0345", Diacritic.IOTA_SUBSCRIPT, UnicodeMode.PRECOMPOSED, True)
    assert letter == "α\u0304\u0313\u0301"

    letter = accent_letter("ρ", Diacritic.ROUGH_BREATHING, UnicodeMode.PRECOMPOSED, True)
    assert letter == "ῥ"

    # illegal diacritic
    letter = accent_letter("ρ", Diacritic.BREVE, UnicodeMode.PRECOMPOSED, True)
    assert letter is None

    # illegal diacritic
    letter = accent_letter("ε", Diacritic.MACRON, UnicodeMode.PRECOMPOSED, True)
    assert letter is None

    # illegal diacritic
    letter = accent_letter("ε", Diacritic.CIRCUMFLEX, UnicodeMode.PRECOMPOSED, True)
    assert letter is None

    letter = accent_letter("ε", Diacritic.GRAVE, UnicodeMode.PRECOMPOSED, True)
    assert letter == "ὲ"

    letter = accent_letter("ι", Diacritic.DIAERESIS, UnicodeMode.PRECOMPOSED, True)
    assert letter == "ϊ"

    letter = accent_letter("υ", Diacritic.DIAERESIS, UnicodeMode.PRECOMPOSED, True)
    assert letter == "ϋ"

    # illegal diacritic
    letter = accent_letter("α", Diacritic.DIAERESIS, UnicodeMode.PRECOMPOSED, True)
    assert letter is None

    letter = accent_letter("ι", Diacritic.BREVE, UnicodeMode.PRECOMPOSED, True)
    assert letter == "ῐ"

    letter = accent_letter("ι", Diacritic.ROUGH_BREATHING, UnicodeMode.PRECOMPOSED, True)
    assert letter == "ἱ"

    letter = accent_letter("ω", Diacritic.CIRCUMFLEX, UnicodeMode.PRECOMPOSED, True)
    assert letter == "ῶ"

    letter = accent_letter("α", Diacritic.MACRON, UnicodeMode.PRECOMPOSED, True)
    assert letter == "ᾱ"

    letter = accent_letter("α", Diacritic.IOTA_SUBSCRIPT, UnicodeMode.PRECOMPOSED, True)
    assert letter == "ᾳ"

    # capital omega with tonos is the last indexed character in the precomposed_codepoints list
    letter = accent_letter("Ω", Diacritic.ACUTE, UnicodeMode.PRECOMPOSED, True)
    assert letter == "\u038F"


def test_pua_diacritics():
    # turn on iota subscript in PUA mode
    letter = accent_letter("α\u0304\u0313\u0301", Diacritic.IOTA_SUBSCRIPT, UnicodeMode.PRECOMPOSED_WITH_PUA, True)
    assert letter == "\ueb07\u0345"

    # toggle_off is False: do nothing, if diacritic is present
    letter = accent_letter("\ueb07\u0345", Diacritic.IOTA_SUBSCRIPT, UnicodeMode.PRECOMPOSED_WITH_PUA, False)
    assert letter == "\ueb07\u0345"


def test_combining_diacritics():
    # combining mode
    letter = accent_letter("α", Diacritic.ACUTE, UnicodeMode.COMBINING_ONLY, True)
    assert letter == "α\u0301"

    # combining mode
    letter = accent_letter("α\u0301", Diacritic.ROUGH_BREATHING, UnicodeMode.COMBINING_ONLY, True)
    assert letter == "α\u0314\u0301"

    # combining mode
    letter = accent_letter("α\u0314\u0301", Diacritic.IOTA_SUBSCRIPT, UnicodeMode.COMBINING_ONLY, True)
    assert letter == "α\u0314\u0301\u0345"

    # combining mode
    letter = accent_letter("α\u0314\u0301\u0345", Diacritic.MACRON, UnicodeMode.COMBINING_ONLY, True)
    assert letter == "α\u0304\u0314\u0301\u0345"

    # combining mode
    letter = accent_letter("α\u0304\u0314\u0301\u0345", Diacritic.ACUTE, UnicodeMode.COMBINING_ONLY, True)
    assert letter == "α\u0304\u0314\u0345"


def test_tonos_oxia():
    # recognize alpha with acute (oxia)
    letter = accent_letter("\u1F71", Diacritic.ACUTE, UnicodeMode.PRECOMPOSED, True)
    assert letter == "α"

    # recognize alpha with acute (tonos)
    letter = accent_letter("\u03AC", Diacritic.ACUTE, UnicodeMode.PRECOMPOSED, True)
    assert letter == "α"

    # alpha with acute (oxia): change to tonos when rewriting
    letter = accent_letter("\u1F71", Diacritic.ACUTE, UnicodeMode.PRECOMPOSED, False)
    assert letter == "\u03AC"

    # recognize epsilon with acute (oxia)
    letter = accent_letter("\u1F73", Diacritic.ACUTE, UnicodeMode.PRECOMPOSED, True)
    assert letter == "ε"

    # recognize epsilon with acute (tonos)
    letter = accent_letter("\u03AD", Diacritic.ACUTE, UnicodeMode.PRECOMPOSED, True)
    assert letter == "ε"

    # epsilon with acute (oxia): change to tonos when rewriting
    letter = accent_letter("\u1F73", Diacritic.ACUTE, UnicodeMode.PRECOMPOSED, False)
    assert letter == "\u03AD"

    # recognize eta with acute (oxia)
    letter = accent_letter("\u1F75", Diacritic.ACUTE, UnicodeMode.PRECOMPOSED, True)
    assert letter == "η"

    # recognize eta with acute (tonos)
    letter = accent_letter("\u03AE", Diacritic.ACUTE, UnicodeMode.PRECOMPOSED, True)
    assert letter == "η"

    # eta with acute (oxia): change to tonos when rewriting
    letter = accent_letter("\u1F75", Diacritic.ACUTE, UnicodeMode.PRECOMPOSED, False)
    assert letter == "\u03AE"

    # recognize iota with acute (oxia)
    letter = accent_letter("\u1F77", Diacritic.ACUTE, UnicodeMode.PRECOMPOSED, True)
    assert letter == "ι"

    # recognize iota with acute (tonos)
    letter = accent_letter("\u03AF", Diacritic.ACUTE, UnicodeMode.PRECOMPOSED, True)
    assert letter == "ι"

    # iota with acute (oxia): change to tonos when rewriting
    letter = accent_letter("\u1F77", Diacritic.ACUTE, UnicodeMode.PRECOMPOSED, False)
    assert letter == "\u03AF"

    # recognize omicron with acute (oxia)
    letter = accent_letter("\u1F79", Diacritic.ACUTE, UnicodeMode.PRECOMPOSED, True)
    assert letter == "ο"

    # recognize omicron with acute (tonos)
    letter = accent_letter("\u03CC", Diacritic.ACUTE, UnicodeMode.PRECOMPOSED, True)
    assert letter == "ο"

    # omicron with acute (oxia): change to tonos when rewriting
    letter = accent_letter("\u1F79", Diacritic.ACUTE, UnicodeMode.PRECOMPOSED, False)
    assert letter == "\u03CC"

    # recognize upsilon with acute (oxia)
    letter = accent_letter("\u1F7B", Diacritic.ACUTE, UnicodeMode.PRECOMPOSED, True)
    assert letter == "υ"

    # recognize upsilon with acute (tonos)
    letter = accent_letter("\u03CD", Diacritic.ACUTE, UnicodeMode.PRECOMPOSED, True)
    assert letter == "υ"

    # upsilon with acute (oxia): change to tonos when rewriting
    letter = accent_letter("\u1F7B", Diacritic.ACUTE, UnicodeMode.PRECOMPOSED, False)
    assert letter == "\u03CD"

    # recognize omega with acute (oxia)
    letter = accent_letter("\u1F7D", Diacritic.ACUTE, UnicodeMode.PRECOMPOSED, True)
    assert letter == "ω"

    # recognize omega with acute (tonos)
    letter = accent_letter("\u03CE", Diacritic.ACUTE, UnicodeMode.PRECOMPOSED, True)
    assert letter == "ω"

    # omega with acute (oxia): change to tonos when rewriting
    letter = accent_letter("\u1F7D", Diacritic.ACUTE, UnicodeMode.PRECOMPOSED, False)
    assert letter == "\u03CE"
