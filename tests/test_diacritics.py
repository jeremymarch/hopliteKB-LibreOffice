# hopliteaccent is added to sys.path in pyproject.toml
from hopliteaccent import accent_letter, Diacritic, UnicodeMode


def test_diacritics():
    letter = accent_letter("α", Diacritic.ACUTE, UnicodeMode.PRECOMPOSED, True)
    assert letter == "ά"

    # pass diacritic parameter as int
    letter = accent_letter("α", 1, UnicodeMode.PRECOMPOSED, True)
    assert letter == "ά"

    # pass diacritic parameter as str
    letter = accent_letter("α", "1", UnicodeMode.PRECOMPOSED, True)
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

    # turn on iota subscript in PUA mode
    letter = accent_letter("α\u0304\u0313\u0301", Diacritic.IOTA_SUBSCRIPT, UnicodeMode.PRECOMPOSED_WITH_PUA, True)
    assert letter == "\ueb07\u0345"

    # toggle_off is False: do nothing, if diacritic is present
    letter = accent_letter("\ueb07\u0345", Diacritic.IOTA_SUBSCRIPT, UnicodeMode.PRECOMPOSED_WITH_PUA, False)
    assert letter == "\ueb07\u0345"

    # combining mode
    letter = accent_letter("α", Diacritic.ACUTE, UnicodeMode.COMBINING_ONLY, True)
    assert letter == "α\u0301"

    # combining mode
    letter = accent_letter("α\u0301", Diacritic.ROUGH_BREATHING, UnicodeMode.COMBINING_ONLY, True)
    assert letter == "α\u0314\u0301"

    # combining mode
    letter = accent_letter("α\u0314\u0301", Diacritic.IOTA_SUBSCRIPT, UnicodeMode.COMBINING_ONLY, True)
    assert letter == "α\u0314\u0301\u0345"

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
