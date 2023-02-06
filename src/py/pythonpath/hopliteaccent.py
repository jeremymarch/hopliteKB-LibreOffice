# -*- coding: utf-8 -*-
#
#  hopliteaccent.py
#  HopliteKB-LibreOffice
#
#  Created by Jeremy March on 12/06/18.
#  Copyright (c) 2018 Jeremy March. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

from enum import IntEnum

# START Public


# unicode modes
class UnicodeMode(IntEnum):
    PRECOMPOSED = 0
    PRECOMPOSED_WITH_PUA = 1
    COMBINING_ONLY = 2
    PRECOMPOSED_HC = 3  # legacy private mode: do not use


# key codes, also indices in cancel_diacritics list
class DiacriticKey(IntEnum):
    ACUTE = 1
    CIRCUMFLEX = 2
    GRAVE = 3
    MACRON = 4
    ROUGH_BREATHING = 5
    SMOOTH_BREATHING = 6
    IOTA_SUBSCRIPT = 7
    # SURROUNDING_PARENTHESES = 8
    DIAERESIS = 9
    BREVE = 10


# bit masks for diacritics bitfield
_MACRON = 1 << 0
_SMOOTH = 1 << 1
_ROUGH = 1 << 2
_ACUTE = 1 << 3
_GRAVE = 1 << 4
_CIRCUMFLEX = 1 << 5
_IOTA_SUB = 1 << 6
_DIAERESIS = 1 << 7
_BREVE = 1 << 8

# turn these diacritics off when adding index diacritic
cancel_diacritics = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
cancel_diacritics[DiacriticKey.ACUTE] = ~(_GRAVE | _CIRCUMFLEX)
cancel_diacritics[DiacriticKey.CIRCUMFLEX] = ~(_ACUTE | _GRAVE | _MACRON | _BREVE)
cancel_diacritics[DiacriticKey.GRAVE] = ~(_ACUTE | _CIRCUMFLEX)
cancel_diacritics[DiacriticKey.MACRON] = ~(_CIRCUMFLEX | _BREVE)
cancel_diacritics[DiacriticKey.ROUGH_BREATHING] = ~(_SMOOTH | _DIAERESIS)
cancel_diacritics[DiacriticKey.SMOOTH_BREATHING] = ~(_ROUGH | _DIAERESIS)
cancel_diacritics[DiacriticKey.IOTA_SUBSCRIPT] = ~0  # nothing
cancel_diacritics[DiacriticKey.DIAERESIS] = ~(_SMOOTH | _ROUGH)
cancel_diacritics[DiacriticKey.BREVE] = ~(_CIRCUMFLEX | _MACRON)

# END Public


# diacritic indices in letters list
class DiacriticIdx(IntEnum):
    NO_DIACRITICS = 0
    PSILI = 1  # smooth
    DASIA = 2  # rough
    OXIA = 3
    PSILI_AND_OXIA = 4
    DASIA_AND_OXIA = 5
    VARIA = 6
    PSILI_AND_VARIA = 7
    DASIA_AND_VARIA = 8
    PERISPOMENI = 9
    PSILI_AND_PERISPOMENI = 10
    DASIA_AND_PERISPOMENI = 11
    YPOGEGRAMMENI = 12
    PSILI_AND_YPOGEGRAMMENI = 13
    DASIA_AND_YPOGEGRAMMENI = 14
    OXIA_AND_YPOGEGRAMMENI = 15
    PSILI_AND_OXIA_AND_YPOGEGRAMMENI = 16
    DASIA_AND_OXIA_AND_YPOGEGRAMMENI = 17
    VARIA_AND_YPOGEGRAMMENI = 18
    PSILI_AND_VARIA_AND_YPOGEGRAMMENI = 19
    DASIA_AND_VARIA_AND_YPOGEGRAMMENI = 20
    PERISPOMENI_AND_YPOGEGRAMMENI = 21
    PSILI_AND_PERISPOMENI_AND_YPOGEGRAMMENI = 22
    DASIA_AND_PERISPOMENI_AND_YPOGEGRAMMENI = 23
    DIALYTIKA = 24
    DIALYTIKA_AND_OXIA = 25
    DIALYTIKA_AND_VARIA = 26
    DIALYTIKA_AND_PERISPOMENON = 27
    MACRON_PRECOMPOSED = 28
    MACRON_AND_SMOOTH = 29
    MACRON_AND_SMOOTH_AND_ACUTE = 30
    MACRON_AND_SMOOTH_AND_GRAVE = 31
    MACRON_AND_ROUGH = 32
    MACRON_AND_ROUGH_AND_ACUTE = 33
    MACRON_AND_ROUGH_AND_GRAVE = 34
    MACRON_AND_ACUTE = 35
    MACRON_AND_GRAVE = 36
    TONOS = 37


# base letter indices
class LetterIdx(IntEnum):
    ALPHA = 0
    EPSILON = 1
    ETA = 2
    IOTA = 3
    OMICRON = 4
    UPSILON = 5
    OMEGA = 6
    ALPHA_CAP = 7
    EPSILON_CAP = 8
    ETA_CAP = 9
    IOTA_CAP = 10
    OMICRON_CAP = 11
    UPSILON_CAP = 12
    OMEGA_CAP = 13


COMBINING_GRAVE = '\u0300'
COMBINING_ACUTE = '\u0301'
COMBINING_CIRCUMFLEX = '\u0342'  # do not use \u0302
COMBINING_MACRON = '\u0304'
COMBINING_BREVE = '\u0306'
COMBINING_DIAERESIS = '\u0308'
COMBINING_SMOOTH_BREATHING = '\u0313'
COMBINING_ROUGH_BREATHING = '\u0314'
COMBINING_IOTA_SUBSCRIPT = '\u0345'
# EM_DASH = '\u2014'
# LEFT_PARENTHESIS = '\u0028'
# RIGHT_PARENTHESIS = '\u0029'
# SPACE = '\u0020'
# EN_DASH = '\u2013'
# HYPHEN = '\u2010'
# COMMA = '\u002C'


# this list determines the order of combining diacritics:
combining_diacritics = [COMBINING_MACRON, COMBINING_BREVE, COMBINING_DIAERESIS, COMBINING_ROUGH_BREATHING, COMBINING_SMOOTH_BREATHING, COMBINING_ACUTE, COMBINING_GRAVE, COMBINING_CIRCUMFLEX, COMBINING_IOTA_SUBSCRIPT]

letters = [
    ['\u03B1', '\u1F00', '\u1F01', '\u1F71', '\u1F04', '\u1F05', '\u1F70', '\u1F02', '\u1F03', '\u1FB6', '\u1F06', '\u1F07', '\u1FB3', '\u1F80', '\u1F81', '\u1FB4', '\u1F84', '\u1F85', '\u1FB2', '\u1F82', '\u1F83', '\u1FB7', '\u1F86', '\u1F87', '\u0000', '\u0000', '\u0000', '\u0000', '\u1FB1', '\uEB04', '\uEB07', '\uEAF3', '\uEB05', '\uEB09', '\uEAF4', '\uEB00', '\uEAF0', '\u03AC'],
    ['\u03B5', '\u1F10', '\u1F11', '\u1F73', '\u1F14', '\u1F15', '\u1F72', '\u1F12', '\u1F13', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u03AD'],
    ['\u03B7', '\u1F20', '\u1F21', '\u1F75', '\u1F24', '\u1F25', '\u1F74', '\u1F22', '\u1F23', '\u1FC6', '\u1F26', '\u1F27', '\u1FC3', '\u1F90', '\u1F91', '\u1FC4', '\u1F94', '\u1F95', '\u1FC2', '\u1F92', '\u1F93', '\u1FC7', '\u1F96', '\u1F97', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u03AE'],
    ['\u03B9', '\u1F30', '\u1F31', '\u1F77', '\u1F34', '\u1F35', '\u1F76', '\u1F32', '\u1F33', '\u1FD6', '\u1F36', '\u1F37', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u03CA', '\u1FD3', '\u1FD2', '\u1FD7', '\u1FD1', '\uEB3C', '\uEB3D', '\uEB54', '\uEB3E', '\uEB3F', '\uEB55', '\uEB39', '\uEB38', '\u03AF'],
    ['\u03BF', '\u1F40', '\u1F41', '\u1F79', '\u1F44', '\u1F45', '\u1F78', '\u1F42', '\u1F43', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u03CC'],
    ['\u03C5', '\u1F50', '\u1F51', '\u1F7B', '\u1F54', '\u1F55', '\u1F7A', '\u1F52', '\u1F53', '\u1FE6', '\u1F56', '\u1F57', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u03CB', '\u1FE3', '\u1FE2', '\u1FE7', '\u1FE1', '\uEB7D', '\uEB7F', '\uEB71', '\uEB7E', '\uEB80', '\uEB75', '\uEB7A', '\uEB6F', '\u03CD'],
    ['\u03C9', '\u1F60', '\u1F61', '\u1F7D', '\u1F64', '\u1F65', '\u1F7C', '\u1F62', '\u1F63', '\u1FF6', '\u1F66', '\u1F67', '\u1FF3', '\u1FA0', '\u1FA1', '\u1FF4', '\u1FA4', '\u1FA5', '\u1FF2', '\u1FA2', '\u1FA3', '\u1FF7', '\u1FA6', '\u1FA7', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u03CE'],
    ['\u0391', '\u1F08', '\u1F09', '\u1FBB', '\u1F0C', '\u1F0D', '\u1FBA', '\u1F0A', '\u1F0B', '\u0000', '\u1F0E', '\u1F0F', '\u1FBC', '\u1F88', '\u1F89', '\u0000', '\u1F8C', '\u1F8D', '\u0000', '\u1F8A', '\u1F8B', '\u0000', '\u1F8E', '\u1F8F', '\u0000', '\u0000', '\u0000', '\u0000', '\u1FB9', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0386'],
    ['\u0395', '\u1F18', '\u1F19', '\u1FC9', '\u1F1C', '\u1F1D', '\u1FC8', '\u1F1A', '\u1F1B', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0388'],
    ['\u0397', '\u1F28', '\u1F29', '\u1FCB', '\u1F2C', '\u1F2D', '\u1FCA', '\u1F2A', '\u1F2B', '\u0000', '\u1F2E', '\u1F2F', '\u1FCC', '\u1F98', '\u1F99', '\u0000', '\u1F9C', '\u1F9D', '\u0000', '\u1F9A', '\u1F9B', '\u0000', '\u1F9E', '\u1F9F', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0389'],
    ['\u0399', '\u1F38', '\u1F39', '\u1FDB', '\u1F3C', '\u1F3D', '\u1FDA', '\u1F3A', '\u1F3B', '\u0000', '\u1F3E', '\u1F3F', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u03AA', '\u0000', '\u0000', '\u0000', '\u1FD9', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u038A'],
    ['\u039F', '\u1F48', '\u1F49', '\u1FF9', '\u1F4C', '\u1F4D', '\u1FF8', '\u1F4A', '\u1F4B', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u038C'],
    ['\u03A5', '\u0000', '\u1F59', '\u1FEB', '\u0000', '\u1F5D', '\u1FEA', '\u0000', '\u1F5B', '\u0000', '\u0000', '\u1F5F', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u03AB', '\u0000', '\u0000', '\u0000', '\u1FE9', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u038E'],
    ['\u03A9', '\u1F68', '\u1F69', '\u1FFB', '\u1F6C', '\u1F6D', '\u1FFA', '\u1F6A', '\u1F6B', '\u0000', '\u1F6E', '\u1F6F', '\u1FFC', '\u1FA8', '\u1FA9', '\u0000', '\u1FAC', '\u1FAD', '\u0000', '\u1FAA', '\u1FAB', '\u0000', '\u1FAE', '\u1FAF', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u038F']]


def get_precomposed_letter(letter_idx, diacritic_bits):
    diacritic_idx = 0

    if diacritic_bits == 0:
        diacritic_idx = DiacriticIdx.NO_DIACRITICS
    elif diacritic_bits == (_SMOOTH):
        diacritic_idx = DiacriticIdx.PSILI
    elif diacritic_bits == (_ROUGH):
        diacritic_idx = DiacriticIdx.DASIA
    elif diacritic_bits == (_ACUTE):
        diacritic_idx = DiacriticIdx.TONOS  # OXIA: tonos is preferred: https://apagreekkeys.org/technicalDetails.html#problems
    elif diacritic_bits == (_SMOOTH | _ACUTE):
        diacritic_idx = DiacriticIdx.PSILI_AND_OXIA
    elif diacritic_bits == (_ROUGH | _ACUTE):
        diacritic_idx = DiacriticIdx.DASIA_AND_OXIA
    elif diacritic_bits == (_GRAVE):
        diacritic_idx = DiacriticIdx.VARIA
    elif diacritic_bits == (_SMOOTH | _GRAVE):
        diacritic_idx = DiacriticIdx.PSILI_AND_VARIA
    elif diacritic_bits == (_ROUGH | _GRAVE):
        diacritic_idx = DiacriticIdx.DASIA_AND_VARIA
    elif diacritic_bits == (_CIRCUMFLEX):
        diacritic_idx = DiacriticIdx.PERISPOMENI
    elif diacritic_bits == (_SMOOTH | _CIRCUMFLEX):
        diacritic_idx = DiacriticIdx.PSILI_AND_PERISPOMENI
    elif diacritic_bits == (_ROUGH | _CIRCUMFLEX):
        diacritic_idx = DiacriticIdx.DASIA_AND_PERISPOMENI
    elif diacritic_bits == (_IOTA_SUB):
        diacritic_idx = DiacriticIdx.YPOGEGRAMMENI
    elif diacritic_bits == (_SMOOTH | _IOTA_SUB):
        diacritic_idx = DiacriticIdx.PSILI_AND_YPOGEGRAMMENI
    elif diacritic_bits == (_ROUGH | _IOTA_SUB):
        diacritic_idx = DiacriticIdx.DASIA_AND_YPOGEGRAMMENI
    elif diacritic_bits == (_ACUTE | _IOTA_SUB):
        diacritic_idx = DiacriticIdx.OXIA_AND_YPOGEGRAMMENI
    elif diacritic_bits == (_SMOOTH | _ACUTE | _IOTA_SUB):
        diacritic_idx = DiacriticIdx.PSILI_AND_OXIA_AND_YPOGEGRAMMENI
    elif diacritic_bits == (_ROUGH | _ACUTE | _IOTA_SUB):
        diacritic_idx = DiacriticIdx.DASIA_AND_OXIA_AND_YPOGEGRAMMENI
    elif diacritic_bits == (_GRAVE | _IOTA_SUB):
        diacritic_idx = DiacriticIdx.VARIA_AND_YPOGEGRAMMENI
    elif diacritic_bits == (_SMOOTH | _GRAVE | _IOTA_SUB):
        diacritic_idx = DiacriticIdx.PSILI_AND_VARIA_AND_YPOGEGRAMMENI
    elif diacritic_bits == (_ROUGH | _GRAVE | _IOTA_SUB):
        diacritic_idx = DiacriticIdx.DASIA_AND_VARIA_AND_YPOGEGRAMMENI
    elif diacritic_bits == (_CIRCUMFLEX | _IOTA_SUB):
        diacritic_idx = DiacriticIdx.PERISPOMENI_AND_YPOGEGRAMMENI
    elif diacritic_bits == (_SMOOTH | _CIRCUMFLEX | _IOTA_SUB):
        diacritic_idx = DiacriticIdx.PSILI_AND_PERISPOMENI_AND_YPOGEGRAMMENI
    elif diacritic_bits == (_ROUGH | _CIRCUMFLEX | _IOTA_SUB):
        diacritic_idx = DiacriticIdx.DASIA_AND_PERISPOMENI_AND_YPOGEGRAMMENI
    elif diacritic_bits == (_DIAERESIS):
        diacritic_idx = DiacriticIdx.DIALYTIKA
    elif diacritic_bits == (_ACUTE | _DIAERESIS):
        diacritic_idx = DiacriticIdx.DIALYTIKA_AND_OXIA
    elif diacritic_bits == (_GRAVE | _DIAERESIS):
        diacritic_idx = DiacriticIdx.DIALYTIKA_AND_VARIA
    elif diacritic_bits == (_CIRCUMFLEX | _DIAERESIS):
        diacritic_idx = DiacriticIdx.DIALYTIKA_AND_PERISPOMENON
    elif diacritic_bits == (_MACRON):
        diacritic_idx = DiacriticIdx.MACRON_PRECOMPOSED
    elif diacritic_bits == (_MACRON | _SMOOTH):
        diacritic_idx = DiacriticIdx.MACRON_AND_SMOOTH
    elif diacritic_bits == (_MACRON | _SMOOTH | _ACUTE):
        diacritic_idx = DiacriticIdx.MACRON_AND_SMOOTH_AND_ACUTE
    elif diacritic_bits == (_MACRON | _SMOOTH | _GRAVE):
        diacritic_idx = DiacriticIdx.MACRON_AND_SMOOTH_AND_GRAVE
    elif diacritic_bits == (_MACRON | _ROUGH):
        diacritic_idx = DiacriticIdx.MACRON_AND_ROUGH
    elif diacritic_bits == (_MACRON | _ROUGH | _ACUTE):
        diacritic_idx = DiacriticIdx.MACRON_AND_ROUGH_AND_ACUTE
    elif diacritic_bits == (_MACRON | _ROUGH | _GRAVE):
        diacritic_idx = DiacriticIdx.MACRON_AND_ROUGH_AND_GRAVE
    elif diacritic_bits == (_MACRON | _ACUTE):
        diacritic_idx = DiacriticIdx.MACRON_AND_ACUTE
    elif diacritic_bits == (_MACRON | _GRAVE):
        diacritic_idx = DiacriticIdx.MACRON_AND_GRAVE
    else:
        diacritic_idx = DiacriticIdx.NO_DIACRITICS  # or set accent = 0 if none of these?

    return letters[letter_idx][diacritic_idx]


def letter_idx_to_UCS2(letter_idx):
    return letters[letter_idx][0]  # first col of each row has base vowels


def make_letter(letter_idx, diacritic_bits, unicode_mode):
    # Use PUA, - almost all precomposing except alpha macron, breathing, accent, iota_sub, if iota_sub use combining
    # Use both, if macron use combining
    # Use only combining accents

    new_letter = ""
    # fallback if macron + one more diacritic
    precomposing_fallback_to_composing = False
    # breve_and_macron = False
    if (unicode_mode == UnicodeMode.PRECOMPOSED and (diacritic_bits & _MACRON) == _MACRON) or (unicode_mode == UnicodeMode.PRECOMPOSED_WITH_PUA and (diacritic_bits & (_MACRON | _DIAERESIS)) == (_MACRON | _DIAERESIS)):
        if (diacritic_bits & ~_MACRON) != 0:  # if any other bits set besides macron
            precomposing_fallback_to_composing = True
    # elif (diacritic_bits & (_BREVE | _MACRON)) == (_BREVE | _MACRON):
    #     breve_and_macron = True
    elif (diacritic_bits & _BREVE) == _BREVE:
        precomposing_fallback_to_composing = True
    elif unicode_mode == UnicodeMode.PRECOMPOSED_HC and (diacritic_bits & _MACRON) == _MACRON:
        # this is legacy for the hoplite challenge app which uses combining macron even if no other diacritics
        precomposing_fallback_to_composing = True

    # special case for breve + macron: use precomposed macron with combining breve - font still doesn't look good
    # if breve_and_macron == True:
    #     diacritic_bits &= ~_BREVE  # turn off
    #     new_letter = get_precomposed_letter(letter_idx, diacritic_bits)  # get with precomposed macron
    #     new_letter += COMBINING_BREVE
    #     return new_letter
    # elif...
    if unicode_mode == UnicodeMode.COMBINING_ONLY or precomposing_fallback_to_composing:

        new_letter = letter_idx_to_UCS2(letter_idx)  # set base letter

        # loop so that order is determined by combining_diacritics list
        for combining_diacritic in combining_diacritics:
            if combining_diacritic == COMBINING_MACRON and (diacritic_bits & _MACRON) == _MACRON:
                new_letter += combining_diacritic
            elif combining_diacritic == COMBINING_BREVE and (diacritic_bits & _BREVE) == _BREVE:
                new_letter += combining_diacritic
            elif combining_diacritic == COMBINING_ROUGH_BREATHING and (diacritic_bits & _ROUGH) == _ROUGH:
                new_letter += combining_diacritic
            elif combining_diacritic == COMBINING_SMOOTH_BREATHING and (diacritic_bits & _SMOOTH) == _SMOOTH:
                new_letter += combining_diacritic
            elif combining_diacritic == COMBINING_ACUTE and (diacritic_bits & _ACUTE) == _ACUTE:
                new_letter += combining_diacritic
            elif combining_diacritic == COMBINING_GRAVE and (diacritic_bits & _GRAVE) == _GRAVE:
                new_letter += combining_diacritic
            elif combining_diacritic == COMBINING_CIRCUMFLEX and (diacritic_bits & _CIRCUMFLEX) == _CIRCUMFLEX:
                new_letter += combining_diacritic
            elif combining_diacritic == COMBINING_IOTA_SUBSCRIPT and (diacritic_bits & _IOTA_SUB) == _IOTA_SUB:
                new_letter += combining_diacritic
            elif combining_diacritic == COMBINING_DIAERESIS and (diacritic_bits & _DIAERESIS) == _DIAERESIS:
                new_letter += combining_diacritic
        return new_letter
    else:
        add_iota_subscript = False
        if unicode_mode == UnicodeMode.PRECOMPOSED_WITH_PUA and (diacritic_bits & (_IOTA_SUB | _MACRON)) == (_IOTA_SUB | _MACRON):
            diacritic_bits &= ~_IOTA_SUB  # so we don't get two iota subscripts
            add_iota_subscript = True

        new_letter = get_precomposed_letter(letter_idx, diacritic_bits)

        if add_iota_subscript is True:
            new_letter += COMBINING_IOTA_SUBSCRIPT

        if len(new_letter) > 0:
            return new_letter
        else:
            return None


# adjusts existing diacritics based on one being added
def update_diacritics(letter_idx, diacritic_bits, diacritic_to_add, toggle_off):
    # keep in order of enum so compiler can optimize switch
    if diacritic_to_add == DiacriticKey.ACUTE:
        if toggle_off and (diacritic_bits & _ACUTE) == _ACUTE:
            diacritic_bits &= ~_ACUTE
        else:
            diacritic_bits |= _ACUTE
        diacritic_bits &= cancel_diacritics[DiacriticKey.ACUTE]  # turn off
    elif diacritic_to_add == DiacriticKey.CIRCUMFLEX:
        if toggle_off and (diacritic_bits & _CIRCUMFLEX) == _CIRCUMFLEX:
            diacritic_bits &= ~_CIRCUMFLEX
        else:
            diacritic_bits |= _CIRCUMFLEX
        diacritic_bits &= cancel_diacritics[DiacriticKey.CIRCUMFLEX]  # turn off
    elif diacritic_to_add == DiacriticKey.GRAVE:
        if toggle_off and (diacritic_bits & _GRAVE) == _GRAVE:
            diacritic_bits &= ~_GRAVE
        else:
            diacritic_bits |= _GRAVE
        diacritic_bits &= cancel_diacritics[DiacriticKey.GRAVE]
    elif diacritic_to_add == DiacriticKey.MACRON:
        if toggle_off and (diacritic_bits & _MACRON) == _MACRON:
            diacritic_bits &= ~_MACRON
        else:
            diacritic_bits |= _MACRON
        diacritic_bits &= cancel_diacritics[DiacriticKey.MACRON]
    elif diacritic_to_add == DiacriticKey.BREVE:
        if toggle_off and (diacritic_bits & _BREVE) == _BREVE:
            diacritic_bits &= ~_BREVE
        else:
            diacritic_bits |= _BREVE
        diacritic_bits &= cancel_diacritics[DiacriticKey.BREVE]
    elif diacritic_to_add == DiacriticKey.ROUGH_BREATHING:
        if toggle_off and (diacritic_bits & _ROUGH) == _ROUGH:
            diacritic_bits &= ~_ROUGH
        else:
            diacritic_bits |= _ROUGH
        diacritic_bits &= cancel_diacritics[DiacriticKey.ROUGH_BREATHING]
    elif diacritic_to_add == DiacriticKey.SMOOTH_BREATHING:
        if toggle_off and (diacritic_bits & _SMOOTH) == _SMOOTH:
            diacritic_bits &= ~_SMOOTH
        else:
            diacritic_bits |= _SMOOTH
        diacritic_bits &= cancel_diacritics[DiacriticKey.SMOOTH_BREATHING]
    elif diacritic_to_add == DiacriticKey.IOTA_SUBSCRIPT:
        if toggle_off and (diacritic_bits & _IOTA_SUB) == _IOTA_SUB:
            diacritic_bits &= ~_IOTA_SUB
        else:
            diacritic_bits |= _IOTA_SUB
        diacritic_bits &= cancel_diacritics[DiacriticKey.IOTA_SUBSCRIPT]
    elif diacritic_to_add == DiacriticKey.DIAERESIS:
        if letter_idx == LetterIdx.IOTA_CAP or letter_idx == LetterIdx.UPSILON_CAP:
            diacritic_bits &= ~(_ACUTE | _GRAVE | _CIRCUMFLEX | _MACRON)

        if toggle_off and (diacritic_bits & _DIAERESIS) == _DIAERESIS:
            diacritic_bits &= ~_DIAERESIS
        else:
            diacritic_bits |= _DIAERESIS
        diacritic_bits &= cancel_diacritics[DiacriticKey.DIAERESIS]

    return diacritic_bits


def is_legal_diacritic_for_letter(letter_idx, diacritic):
    # match these strings to the arguments in the accelerators
    if diacritic == DiacriticKey.CIRCUMFLEX:
        if letter_idx != LetterIdx.ALPHA and letter_idx != LetterIdx.ETA and letter_idx != LetterIdx.IOTA and letter_idx != LetterIdx.UPSILON and letter_idx != LetterIdx.OMEGA:  # and letter_idx != LetterIdx.ALPHA_CAP and letter_idx != LetterIdx.ETA_CAP and letter_idx != LetterIdx.IOTA_CAP and letter_idx != LetterIdx.UPSILON_CAP and letter_idx != LetterIdx.OMEGA_CAP:
            return False
    elif diacritic == DiacriticKey.MACRON:
        if letter_idx != LetterIdx.ALPHA and letter_idx != LetterIdx.IOTA and letter_idx != LetterIdx.UPSILON and letter_idx != LetterIdx.ALPHA_CAP and letter_idx != LetterIdx.IOTA_CAP and letter_idx != LetterIdx.UPSILON_CAP:
            return False
    elif diacritic == DiacriticKey.BREVE:
        if letter_idx != LetterIdx.ALPHA and letter_idx != LetterIdx.IOTA and letter_idx != LetterIdx.UPSILON and letter_idx != LetterIdx.ALPHA_CAP and letter_idx != LetterIdx.IOTA_CAP and letter_idx != LetterIdx.UPSILON_CAP:
            return False
    elif diacritic == DiacriticKey.IOTA_SUBSCRIPT:
        if letter_idx != LetterIdx.ALPHA and letter_idx != LetterIdx.ETA and letter_idx != LetterIdx.OMEGA and letter_idx != LetterIdx.ALPHA_CAP and letter_idx != LetterIdx.ETA_CAP and letter_idx != LetterIdx.OMEGA_CAP:
            return False
    elif diacritic == DiacriticKey.DIAERESIS:
        if letter_idx != LetterIdx.IOTA and letter_idx != LetterIdx.UPSILON and letter_idx != LetterIdx.IOTA_CAP and letter_idx != LetterIdx.UPSILON_CAP:
            return False
    return True


# a hash table could save us from looping through all this
# we don't want to analyze via canonical decomposition because PUA characters are not canonical
def analyze_precomposed_letter(letter):
    for letter_idx in range(0, len(LetterIdx)):
        for diacritic_idx in range(0, len(DiacriticIdx)):
            if letter[0] == letters[letter_idx][diacritic_idx]:
                return (letter_idx, diacritic_idx)
    return (None, None)


def precomposed_index_to_bitmask(diacritic_idx, diacritic_bits):
    # don't initialize to false here because diacriticMask could have combining accents already set to true
    # make sure this is in order of enum so compiler can optimize switch
    if diacritic_idx == DiacriticIdx.PSILI:
        diacritic_bits |= _SMOOTH
    elif diacritic_idx == DiacriticIdx.DASIA:
        diacritic_bits |= _ROUGH
    elif diacritic_idx == DiacriticIdx.OXIA:
        diacritic_bits |= _ACUTE
    elif diacritic_idx == DiacriticIdx.PSILI_AND_OXIA:
        diacritic_bits |= (_SMOOTH | _ACUTE)
    elif diacritic_idx == DiacriticIdx.DASIA_AND_OXIA:
        diacritic_bits |= (_ROUGH | _ACUTE)
    elif diacritic_idx == DiacriticIdx.VARIA:
        diacritic_bits |= _GRAVE
    elif diacritic_idx == DiacriticIdx.PSILI_AND_VARIA:
        diacritic_bits |= (_SMOOTH | _GRAVE)
    elif diacritic_idx == DiacriticIdx.DASIA_AND_VARIA:
        diacritic_bits |= (_ROUGH | _GRAVE)
    elif diacritic_idx == DiacriticIdx.PERISPOMENI:
        diacritic_bits |= _CIRCUMFLEX
    elif diacritic_idx == DiacriticIdx.PSILI_AND_PERISPOMENI:
        diacritic_bits |= (_SMOOTH | _CIRCUMFLEX)
    elif diacritic_idx == DiacriticIdx.DASIA_AND_PERISPOMENI:
        diacritic_bits |= (_ROUGH | _CIRCUMFLEX)
    elif diacritic_idx == DiacriticIdx.YPOGEGRAMMENI:
        diacritic_bits |= _IOTA_SUB
    elif diacritic_idx == DiacriticIdx.PSILI_AND_YPOGEGRAMMENI:
        diacritic_bits |= (_SMOOTH | _IOTA_SUB)
    elif diacritic_idx == DiacriticIdx.DASIA_AND_YPOGEGRAMMENI:
        diacritic_bits |= (_ROUGH | _IOTA_SUB)
    elif diacritic_idx == DiacriticIdx.OXIA_AND_YPOGEGRAMMENI:
        diacritic_bits |= (_ACUTE | _IOTA_SUB)
    elif diacritic_idx == DiacriticIdx.PSILI_AND_OXIA_AND_YPOGEGRAMMENI:
        diacritic_bits |= (_SMOOTH | _ACUTE | _IOTA_SUB)
    elif diacritic_idx == DiacriticIdx.DASIA_AND_OXIA_AND_YPOGEGRAMMENI:
        diacritic_bits |= (_ROUGH | _ACUTE | _IOTA_SUB)
    elif diacritic_idx == DiacriticIdx.VARIA_AND_YPOGEGRAMMENI:
        diacritic_bits |= (_GRAVE | _IOTA_SUB)
    elif diacritic_idx == DiacriticIdx.PSILI_AND_VARIA_AND_YPOGEGRAMMENI:
        diacritic_bits |= (_SMOOTH | _GRAVE | _IOTA_SUB)
    elif diacritic_idx == DiacriticIdx.DASIA_AND_VARIA_AND_YPOGEGRAMMENI:
        diacritic_bits |= (_ROUGH | _GRAVE | _IOTA_SUB)
    elif diacritic_idx == DiacriticIdx.PERISPOMENI_AND_YPOGEGRAMMENI:
        diacritic_bits |= (_CIRCUMFLEX | _IOTA_SUB)
    elif diacritic_idx == DiacriticIdx.PSILI_AND_PERISPOMENI_AND_YPOGEGRAMMENI:
        diacritic_bits |= (_SMOOTH | _CIRCUMFLEX | _IOTA_SUB)
    elif diacritic_idx == DiacriticIdx.DASIA_AND_PERISPOMENI_AND_YPOGEGRAMMENI:
        diacritic_bits |= (_ROUGH | _CIRCUMFLEX | _IOTA_SUB)
    elif diacritic_idx == DiacriticIdx.DIALYTIKA:
        diacritic_bits |= _DIAERESIS
    elif diacritic_idx == DiacriticIdx.DIALYTIKA_AND_OXIA:
        diacritic_bits |= (_DIAERESIS | _ACUTE)
    elif diacritic_idx == DiacriticIdx.DIALYTIKA_AND_VARIA:
        diacritic_bits |= (_DIAERESIS | _GRAVE)
    elif diacritic_idx == DiacriticIdx.DIALYTIKA_AND_PERISPOMENON:
        diacritic_bits |= (_DIAERESIS | _CIRCUMFLEX)
    elif diacritic_idx == DiacriticIdx.MACRON_PRECOMPOSED:
        diacritic_bits |= _MACRON
    elif diacritic_idx == DiacriticIdx.MACRON_AND_SMOOTH:
        diacritic_bits |= (_MACRON | _SMOOTH)
    elif diacritic_idx == DiacriticIdx.MACRON_AND_SMOOTH_AND_ACUTE:
        diacritic_bits |= (_MACRON | _SMOOTH | _ACUTE)
    elif diacritic_idx == DiacriticIdx.MACRON_AND_SMOOTH_AND_GRAVE:
        diacritic_bits |= (_MACRON | _SMOOTH | _GRAVE)
    elif diacritic_idx == DiacriticIdx.MACRON_AND_ROUGH:
        diacritic_bits |= (_MACRON | _ROUGH)
    elif diacritic_idx == DiacriticIdx.MACRON_AND_ROUGH_AND_ACUTE:
        diacritic_bits |= (_MACRON | _ROUGH | _ACUTE)
    elif diacritic_idx == DiacriticIdx.MACRON_AND_ROUGH_AND_GRAVE:
        diacritic_bits |= (_MACRON | _ROUGH | _GRAVE)
    elif diacritic_idx == DiacriticIdx.MACRON_AND_ACUTE:
        diacritic_bits |= (_MACRON | _ACUTE)
    elif diacritic_idx == DiacriticIdx.MACRON_AND_GRAVE:
        diacritic_bits |= (_MACRON | _GRAVE)
    elif diacritic_idx == DiacriticIdx.TONOS:  # we conflate tonos and acute
        diacritic_bits |= _ACUTE
    return diacritic_bits


# returns a tuple (letter_idx, diacritics_bits) or (None, None)
def analyze_letter(letter):
    # fix me in c version, better here
    diacritic_bits = 0

    letter_len = len(letter)
    if letter_len > 1:
        for le in letter:  # (int j = 1; j <= MAX_COMBINING && i + j < len; j++)
            if le == COMBINING_ROUGH_BREATHING:
                diacritic_bits |= _ROUGH
            elif le == COMBINING_SMOOTH_BREATHING:
                diacritic_bits |= _SMOOTH
            elif le == COMBINING_ACUTE:
                diacritic_bits |= _ACUTE
            elif le == COMBINING_GRAVE:
                diacritic_bits |= _GRAVE
            elif le == COMBINING_CIRCUMFLEX:
                diacritic_bits |= _CIRCUMFLEX
            elif le == COMBINING_MACRON:
                diacritic_bits |= _MACRON
            elif le == COMBINING_BREVE:
                diacritic_bits |= _BREVE
            elif le == COMBINING_IOTA_SUBSCRIPT:
                diacritic_bits |= _IOTA_SUB
            elif le == COMBINING_DIAERESIS:
                diacritic_bits |= _DIAERESIS
            else:
                continue  # continue, not break because first letter is not combining

    (letter_idx, diacritic_idx) = analyze_precomposed_letter(letter)
    if letter_idx is None:
        return (None, None)

    diacritic_bits = precomposed_index_to_bitmask(diacritic_idx, diacritic_bits)

    return (letter_idx, diacritic_bits)


# letter:       letter to which we are adding the diacritic
# diacritic:    diacritic to add
# unicode_mode: unicode mode to use
# toggle_off:   whether we want to toggle off the diacritic if it is already present on the letter
def accent_letter(letter, diacritic, unicode_mode, toggle_off):
    try:
        if int(unicode_mode) < 0 or int(unicode_mode) > 3:
            unicode_mode = UnicodeMode.PRECOMPOSED
    except ValueError:
        unicode_mode = UnicodeMode.PRECOMPOSED

    # bAddSpacingDiacriticIfNotLegal = False  # for now

    # handle rho
    rho = '\u03c1'
    rho_with_dasia = '\u1fe5'
    rho_with_psili = '\u1fe4'
    rho_cap = '\u03a1'
    rho_cap_with_dasia = '\u1fec'

    if letter == rho and diacritic == DiacriticKey.ROUGH_BREATHING:
        return rho_with_dasia
    elif letter == rho_with_dasia and diacritic == DiacriticKey.ROUGH_BREATHING:
        return rho
    elif letter == rho_cap and diacritic == DiacriticKey.ROUGH_BREATHING:
        return rho_cap_with_dasia
    elif letter == rho_cap_with_dasia and diacritic == DiacriticKey.ROUGH_BREATHING:
        return rho_cap
    elif letter == rho_with_psili and diacritic == DiacriticKey.ROUGH_BREATHING:
        return rho_with_dasia
    elif letter == rho and diacritic == DiacriticKey.SMOOTH_BREATHING:
        return rho_with_psili
    elif letter == rho_with_psili and diacritic == DiacriticKey.SMOOTH_BREATHING:
        return rho
    elif letter == rho_with_dasia and diacritic == DiacriticKey.SMOOTH_BREATHING:
        return rho_with_psili

    # 1. analyze the letter to be accented
    (letter_idx, diacritic_bits) = analyze_letter(letter)
    if letter_idx is None:
        return None

    # 2. is it legal to add this diacritic?
    if is_legal_diacritic_for_letter(letter_idx, diacritic) is False:
        return None

    # 3. add new diacritic to the existing diacritics, making adjustments accordingly
    diacritic_bits = update_diacritics(letter_idx, diacritic_bits, diacritic, toggle_off)

    # 4. make and return the new character
    new_letter = make_letter(letter_idx, diacritic_bits, unicode_mode)
    if new_letter is None:
        return None
    else:
        return new_letter
