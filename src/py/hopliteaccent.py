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

#THESE ARE MEANT TO BE ACCESSED OUTSIDE:

#unicode modes
PRECOMPOSED_MODE          = 0
PRECOMPOSED_WITH_PUA_MODE = 1
COMBINING_ONLY_MODE       = 2
PRECOMPOSED_HC_MODE       = 3

#key codes, also indexes in cancelDiacritics array
#kNO_ACCENT       = 0
kACUTE            = 1
kCIRCUMFLEX       = 2
kGRAVE            = 3
kMACRON           = 4
kROUGH_BREATHING  = 5
kSMOOTH_BREATHING = 6
kIOTA_SUBSCRIPT   = 7
#kSURROUNDING_PARENTHESES = 8
kDIAERESIS        = 9
kBREVE            = 10

#bit masks for diacritics bitfield
_MACRON     = 1 << 0
_SMOOTH     = 1 << 1
_ROUGH      = 1 << 2
_ACUTE      = 1 << 3
_GRAVE      = 1 << 4
_CIRCUMFLEX = 1 << 5
_IOTA_SUB   = 1 << 6
_DIAERESIS  = 1 << 7
_BREVE      = 1 << 8 

#turn these diacritics off when adding index diacritic
cancelDiacritics = [0,0,0,0,0,0,0,0,0,0,0]
cancelDiacritics[kACUTE]            = ~(_GRAVE | _CIRCUMFLEX)
cancelDiacritics[kCIRCUMFLEX]       = ~(_ACUTE | _GRAVE | _MACRON | _BREVE)
cancelDiacritics[kGRAVE]            = ~(_ACUTE | _CIRCUMFLEX)
cancelDiacritics[kMACRON]           = ~(_CIRCUMFLEX | _BREVE)
cancelDiacritics[kROUGH_BREATHING]  = ~(_SMOOTH | _DIAERESIS)
cancelDiacritics[kSMOOTH_BREATHING] = ~(_ROUGH | _DIAERESIS)
cancelDiacritics[kIOTA_SUBSCRIPT]   = ~0 #nothing
cancelDiacritics[kDIAERESIS]        = ~(_SMOOTH | _ROUGH)
cancelDiacritics[kBREVE]            = ~(_CIRCUMFLEX | _MACRON)

#END ACCESSED OUTSIDE





#diacritic indices in letters array
NORMAL = 0
PSILI  = 1                               #smooth
DASIA  = 2                               #rough
OXIA   = 3
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
#ifdef ALLOW_PRIVATE_USE_AREA
MACRON_AND_SMOOTH = 29
MACRON_AND_SMOOTH_AND_ACUTE = 30
MACRON_AND_SMOOTH_AND_GRAVE = 31
MACRON_AND_ROUGH = 32
MACRON_AND_ROUGH_AND_ACUTE = 33
MACRON_AND_ROUGH_AND_GRAVE = 34
MACRON_AND_ACUTE = 35
MACRON_AND_GRAVE = 36
TONOS = 37
#endif
NUM_ACCENT_CODES = 38

#base letter indices
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
NUM_VOWEL_CODES = 14


COMBINING_GRAVE            = '\u0300'
COMBINING_ACUTE            = '\u0301'
COMBINING_CIRCUMFLEX       = '\u0342' # do not use 0x0302
COMBINING_MACRON           = '\u0304'
COMBINING_BREVE            = '\u0306'
COMBINING_DIAERESIS        = '\u0308'
COMBINING_SMOOTH_BREATHING = '\u0313'
COMBINING_ROUGH_BREATHING  = '\u0314'
COMBINING_IOTA_SUBSCRIPT   = '\u0345'
# EM_DASH                         0x2014
# LEFT_PARENTHESIS                0x0028
# RIGHT_PARENTHESIS               0x0029
# SPACE                           0x0020
# EN_DASH                         0x2013
# HYPHEN                          0x2010
# COMMA                           0x002C


# this list determines the order of combining diacritics:
combiningAccents = [ COMBINING_MACRON, COMBINING_BREVE, COMBINING_DIAERESIS, COMBINING_ROUGH_BREATHING, COMBINING_SMOOTH_BREATHING, COMBINING_ACUTE, COMBINING_GRAVE, COMBINING_CIRCUMFLEX, COMBINING_IOTA_SUBSCRIPT ]

letters = [ [ '\u03B1', '\u1F00', '\u1F01', '\u1F71', '\u1F04', '\u1F05', '\u1F70', '\u1F02', '\u1F03', '\u1FB6', '\u1F06', '\u1F07', '\u1FB3', '\u1F80', '\u1F81', '\u1FB4', '\u1F84', '\u1F85', '\u1FB2', '\u1F82', '\u1F83', '\u1FB7', '\u1F86', '\u1F87', '\u0000', '\u0000', '\u0000', '\u0000', '\u1FB1', '\uEB04', '\uEB07', '\uEAF3', '\uEB05', '\uEB09', '\uEAF4', '\uEB00', '\uEAF0', '\u03AC' ], 
[ '\u03B5', '\u1F10', '\u1F11', '\u1F73', '\u1F14', '\u1F15', '\u1F72', '\u1F12', '\u1F13', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u03AD' ], 
[ '\u03B7', '\u1F20', '\u1F21', '\u1F75', '\u1F24', '\u1F25', '\u1F74', '\u1F22', '\u1F23', '\u1FC6', '\u1F26', '\u1F27', '\u1FC3', '\u1F90', '\u1F91', '\u1FC4', '\u1F94', '\u1F95', '\u1FC2', '\u1F92', '\u1F93', '\u1FC7', '\u1F96', '\u1F97', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u03AE' ], 
[ '\u03B9', '\u1F30', '\u1F31', '\u1F77', '\u1F34', '\u1F35', '\u1F76', '\u1F32', '\u1F33', '\u1FD6', '\u1F36', '\u1F37', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u03CA', '\u1FD3', '\u1FD2', '\u1FD7', '\u1FD1', '\uEB3C', '\uEB3D', '\uEB54', '\uEB3E', '\uEB3F', '\uEB55', '\uEB39', '\uEB38', '\u03AF' ], 
[ '\u03BF', '\u1F40', '\u1F41', '\u1F79', '\u1F44', '\u1F45', '\u1F78', '\u1F42', '\u1F43', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u03CC' ], 
[ '\u03C5', '\u1F50', '\u1F51', '\u1F7B', '\u1F54', '\u1F55', '\u1F7A', '\u1F52', '\u1F53', '\u1FE6', '\u1F56', '\u1F57', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u03CB', '\u1FE3', '\u1FE2', '\u1FE7', '\u1FE1', '\uEB7D', '\uEB7F', '\uEB71', '\uEB7E', '\uEB80', '\uEB75', '\uEB7A', '\uEB6F', '\u03CD' ], 
[ '\u03C9', '\u1F60', '\u1F61', '\u1F7D', '\u1F64', '\u1F65', '\u1F7C', '\u1F62', '\u1F63', '\u1FF6', '\u1F66', '\u1F67', '\u1FF3', '\u1FA0', '\u1FA1', '\u1FF4', '\u1FA4', '\u1FA5', '\u1FF2', '\u1FA2', '\u1FA3', '\u1FF7', '\u1FA6', '\u1FA7', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u03CE' ], 
[ '\u0391', '\u1F08', '\u1F09', '\u1FBB', '\u1F0C', '\u1F0D', '\u1FBA', '\u1F0A', '\u1F0B', '\u0000', '\u1F0E', '\u1F0F', '\u1FBC', '\u1F88', '\u1F89', '\u0000', '\u1F8C', '\u1F8D', '\u0000', '\u1F8A', '\u1F8B', '\u0000', '\u1F8E', '\u1F8F', '\u0000', '\u0000', '\u0000', '\u0000', '\u1FB9', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0386' ], 
[ '\u0395', '\u1F18', '\u1F19', '\u1FC9', '\u1F1C', '\u1F1D', '\u1FC8', '\u1F1A', '\u1F1B', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0388' ], 
[ '\u0397', '\u1F28', '\u1F29', '\u1FCB', '\u1F2C', '\u1F2D', '\u1FCA', '\u1F2A', '\u1F2B', '\u0000', '\u1F2E', '\u1F2F', '\u1FCC', '\u1F98', '\u1F99', '\u0000', '\u1F9C', '\u1F9D', '\u0000', '\u1F9A', '\u1F9B', '\u0000', '\u1F9E', '\u1F9F', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0389' ], 
[ '\u0399', '\u1F38', '\u1F39', '\u1FDB', '\u1F3C', '\u1F3D', '\u1FDA', '\u1F3A', '\u1F3B', '\u0000', '\u1F3E', '\u1F3F', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u03AA', '\u0000', '\u0000', '\u0000', '\u1FD9', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u038A' ], 
[ '\u039F', '\u1F48', '\u1F49', '\u1FF9', '\u1F4C', '\u1F4D', '\u1FF8', '\u1F4A', '\u1F4B', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u038C' ], 
[ '\u03A5', '\u0000', '\u1F59', '\u1FEB', '\u0000', '\u1F5D', '\u1FEA', '\u0000', '\u1F5B', '\u0000', '\u0000', '\u1F5F', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u03AB', '\u0000', '\u0000', '\u0000', '\u1FE9', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u038E' ],
[ '\u03A9', '\u1F68', '\u1F69', '\u1FFB', '\u1F6C', '\u1F6D', '\u1FFA', '\u1F6A', '\u1F6B', '\u0000', '\u1F6E', '\u1F6F', '\u1FFC', '\u1FA8', '\u1FA9', '\u0000', '\u1FAC', '\u1FAD', '\u0000', '\u1FAA', '\u1FAB', '\u0000', '\u1FAE', '\u1FAF', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u0000', '\u038F' ] ]

def getPrecomposedLetter(letterIndex, diacriticBits):
    accentIndex = 0

    if diacriticBits == 0:
        accentIndex = NORMAL
    elif diacriticBits == (_SMOOTH):
        accentIndex = PSILI
    elif diacriticBits == (_ROUGH):
        accentIndex = DASIA
    elif diacriticBits == (_ACUTE):
        accentIndex = TONOS #OXIA, tonos is preferred: https://apagreekkeys.org/technicalDetails.html#problems
    elif diacriticBits == (_SMOOTH | _ACUTE):
        accentIndex = PSILI_AND_OXIA
    elif diacriticBits == (_ROUGH | _ACUTE):
        accentIndex = DASIA_AND_OXIA
    elif diacriticBits == (_GRAVE):
        accentIndex = VARIA
    elif diacriticBits == (_SMOOTH | _GRAVE):
        accentIndex = PSILI_AND_VARIA
    elif diacriticBits == (_ROUGH | _GRAVE):
        accentIndex = DASIA_AND_VARIA
    elif diacriticBits == (_CIRCUMFLEX):
        accentIndex = PERISPOMENI
    elif diacriticBits == (_SMOOTH | _CIRCUMFLEX):
        accentIndex = PSILI_AND_PERISPOMENI
    elif diacriticBits == (_ROUGH | _CIRCUMFLEX):
        accentIndex = DASIA_AND_PERISPOMENI
    elif diacriticBits == (_IOTA_SUB):
        accentIndex = YPOGEGRAMMENI
    elif diacriticBits == (_SMOOTH | _IOTA_SUB):
        accentIndex = PSILI_AND_YPOGEGRAMMENI
    elif diacriticBits == (_ROUGH | _IOTA_SUB):
        accentIndex = DASIA_AND_YPOGEGRAMMENI
    elif diacriticBits == (_ACUTE | _IOTA_SUB):
        accentIndex = OXIA_AND_YPOGEGRAMMENI
    elif diacriticBits == (_SMOOTH | _ACUTE | _IOTA_SUB):
        accentIndex = PSILI_AND_OXIA_AND_YPOGEGRAMMENI
    elif diacriticBits == (_ROUGH | _ACUTE | _IOTA_SUB):
        accentIndex = DASIA_AND_OXIA_AND_YPOGEGRAMMENI
    elif diacriticBits == (_GRAVE | _IOTA_SUB):
        accentIndex = VARIA_AND_YPOGEGRAMMENI
    elif diacriticBits == (_SMOOTH | _GRAVE | _IOTA_SUB):
        accentIndex = PSILI_AND_VARIA_AND_YPOGEGRAMMENI
    elif diacriticBits == (_ROUGH | _GRAVE | _IOTA_SUB):
        accentIndex = DASIA_AND_VARIA_AND_YPOGEGRAMMENI
    elif diacriticBits == (_CIRCUMFLEX | _IOTA_SUB):
        accentIndex = PERISPOMENI_AND_YPOGEGRAMMENI
    elif diacriticBits == (_SMOOTH | _CIRCUMFLEX | _IOTA_SUB):
        accentIndex = PSILI_AND_PERISPOMENI_AND_YPOGEGRAMMENI
    elif diacriticBits == (_ROUGH | _CIRCUMFLEX | _IOTA_SUB):
        accentIndex = DASIA_AND_PERISPOMENI_AND_YPOGEGRAMMENI
    elif diacriticBits == (_DIAERESIS):
        accentIndex = DIALYTIKA
    elif diacriticBits == (_ACUTE | _DIAERESIS):
        accentIndex = DIALYTIKA_AND_OXIA
    elif diacriticBits == (_GRAVE | _DIAERESIS):
        accentIndex = DIALYTIKA_AND_VARIA
    elif diacriticBits == (_CIRCUMFLEX | _DIAERESIS):
        accentIndex = DIALYTIKA_AND_PERISPOMENON
    elif diacriticBits == (_MACRON):
        accentIndex = MACRON_PRECOMPOSED
#ifdef ALLOW_PRIVATE_USE_AREA
    elif diacriticBits == (_MACRON | _SMOOTH):
        accentIndex = MACRON_AND_SMOOTH
    elif diacriticBits == (_MACRON | _SMOOTH | _ACUTE):
        accentIndex = MACRON_AND_SMOOTH_AND_ACUTE
    elif diacriticBits == (_MACRON | _SMOOTH | _GRAVE):
        accentIndex = MACRON_AND_SMOOTH_AND_GRAVE
    elif diacriticBits == (_MACRON | _ROUGH):
        accentIndex = MACRON_AND_ROUGH
    elif diacriticBits == (_MACRON | _ROUGH | _ACUTE):
        accentIndex = MACRON_AND_ROUGH_AND_ACUTE
    elif diacriticBits == (_MACRON | _ROUGH | _GRAVE):
        accentIndex = MACRON_AND_ROUGH_AND_GRAVE
    elif diacriticBits == (_MACRON | _ACUTE):
        accentIndex = MACRON_AND_ACUTE
    elif diacriticBits == (_MACRON | _GRAVE):
        accentIndex = MACRON_AND_GRAVE
#endif
    else:
        accentIndex = NORMAL #or set accent = 0 if none of these?

    return letters[letterIndex][accentIndex]


def letterCodeToUCS2(l):
    return letters[l][0] #first col of each row has base vowels


def makeLetter(letterIndex, diacriticBits, unicodeMode):
    #Use PUA, - almost all precomposing except alpha macron, breathing, accent, iota_sub, if iota_sub use combining
    #Use both, if macron use combining
    #Use only combining accents

    newLetter = ""
    #fallback if macron + one more diacritic
    precomposingFallbackToComposing = False
    breveAndMacron = False
    if (unicodeMode == PRECOMPOSED_MODE and (diacriticBits & _MACRON) == _MACRON) or (unicodeMode == PRECOMPOSED_WITH_PUA_MODE and (diacriticBits & (_MACRON | _DIAERESIS)) == (_MACRON | _DIAERESIS)):
        if (diacriticBits & ~_MACRON) != 0: #if any other bits set besides macron
            precomposingFallbackToComposing = True
    # elif (letterCodeAndBitMask[1] & (_BREVE | _MACRON)) == (_BREVE | _MACRON):
    #     breveAndMacron = True
    elif (diacriticBits & _BREVE) == _BREVE:
        precomposingFallbackToComposing = True
    elif unicodeMode == PRECOMPOSED_HC_MODE and (diacriticBits & _MACRON) == _MACRON:
        #this is legacy for the hoplite challenge app which uses combining macron even if no other diacritics
        precomposingFallbackToComposing = True

    #special case for breve + macron: use precomposed macron with combining breve - font still doesn't look good
    # if breveAndMacron == True:
    #     letterCodeAndBitMask[1] &= ~_BREVE #turn off
    #     newLetter = getPrecomposedLetter(letterCodeAndBitMask) #get with precomposed macron
    #     newLetter += COMBINING_BREVE
    #     return newLetter
    # elif...
    if unicodeMode == COMBINING_ONLY_MODE or precomposingFallbackToComposing:

        newLetter = letterCodeToUCS2(letterIndex) #set base letter

        #loop so that order is determined by combiningAccents array
        for k in combiningAccents:
            if k == COMBINING_MACRON and (diacriticBits & _MACRON) == _MACRON:
                newLetter += k
            elif k == COMBINING_BREVE and (diacriticBits & _BREVE) == _BREVE:
                newLetter += k
            elif k == COMBINING_ROUGH_BREATHING and (diacriticBits & _ROUGH) == _ROUGH:
                newLetter += k
            elif k == COMBINING_SMOOTH_BREATHING and (diacriticBits & _SMOOTH) == _SMOOTH:
                newLetter += k
            elif k == COMBINING_ACUTE and (diacriticBits & _ACUTE) == _ACUTE:
                newLetter += k
            elif k == COMBINING_GRAVE and (diacriticBits & _GRAVE) == _GRAVE:
                newLetter += k
            elif k == COMBINING_CIRCUMFLEX and (diacriticBits & _CIRCUMFLEX) == _CIRCUMFLEX:
                newLetter += k
            elif k == COMBINING_IOTA_SUBSCRIPT and (diacriticBits & _IOTA_SUB) == _IOTA_SUB:
                newLetter += k
            elif k == COMBINING_DIAERESIS and (diacriticBits & _DIAERESIS) == _DIAERESIS:
                newLetter += k
        return newLetter
    else:
        addIotaSubscript = False
        if unicodeMode == PRECOMPOSED_WITH_PUA_MODE and (diacriticBits & (_IOTA_SUB | _MACRON)) == (_IOTA_SUB | _MACRON):
            diacriticBits &= ~_IOTA_SUB #so we don't get two iota subscripts
            addIotaSubscript = True

        newLetter = getPrecomposedLetter(letterIndex, diacriticBits)

        if addIotaSubscript == True:
            newLetter += COMBINING_IOTA_SUBSCRIPT
        
        if len(newLetter) > 0:
            return newLetter
        else:
            return None


#adjusts existing diacritics based on one being added
def updateDiacritics(letterIndex, diacriticBits, accentToAdd, toggleOff):
    #keep in order of enum so compiler can optimize switch
    if accentToAdd == kACUTE:
        if toggleOff and (diacriticBits & _ACUTE) == _ACUTE:
            diacriticBits &= ~_ACUTE
        else:
            diacriticBits |= _ACUTE
        diacriticBits &= cancelDiacritics[kACUTE] #turn off
    elif accentToAdd == kCIRCUMFLEX:
        if toggleOff and (diacriticBits & _CIRCUMFLEX) == _CIRCUMFLEX:
            diacriticBits &= ~_CIRCUMFLEX
        else:
            diacriticBits |= _CIRCUMFLEX
        diacriticBits &= cancelDiacritics[kCIRCUMFLEX] #turn off. fix me in c version, replace breve
    elif accentToAdd == kGRAVE:
        if toggleOff and (diacriticBits & _GRAVE) == _GRAVE:
            diacriticBits &= ~_GRAVE
        else:
            diacriticBits |= _GRAVE
        diacriticBits &= cancelDiacritics[kGRAVE]
    elif accentToAdd == kMACRON:
        if toggleOff and (diacriticBits & _MACRON) == _MACRON:
            diacriticBits &= ~_MACRON
        else:
            diacriticBits |= _MACRON
        diacriticBits &= cancelDiacritics[kMACRON]
    elif accentToAdd == kBREVE:
        if toggleOff and (diacriticBits & _BREVE) == _BREVE:
            diacriticBits &= ~_BREVE
        else:
            diacriticBits |= _BREVE
        diacriticBits &= cancelDiacritics[kBREVE]
    elif accentToAdd == kROUGH_BREATHING:
        if toggleOff and (diacriticBits & _ROUGH) == _ROUGH:
            diacriticBits &= ~_ROUGH
        else:
            diacriticBits |= _ROUGH
        diacriticBits &= cancelDiacritics[kROUGH_BREATHING]
    elif accentToAdd == kSMOOTH_BREATHING:
        if toggleOff and (diacriticBits & _SMOOTH) == _SMOOTH:
            diacriticBits &= ~_SMOOTH
        else:
            diacriticBits |= _SMOOTH
        diacriticBits &= cancelDiacritics[kSMOOTH_BREATHING]
    elif accentToAdd == kIOTA_SUBSCRIPT:
        if toggleOff and (diacriticBits & _IOTA_SUB) == _IOTA_SUB:
            diacriticBits &= ~_IOTA_SUB
        else:
            diacriticBits |= _IOTA_SUB
        diacriticBits &= cancelDiacritics[kIOTA_SUBSCRIPT]
    elif accentToAdd == kDIAERESIS:
        if letterIndex == IOTA_CAP or letterIndex == UPSILON_CAP:
            diacriticBits &= ~(_ACUTE | _GRAVE | _CIRCUMFLEX | _MACRON)

        if toggleOff and (diacriticBits & _DIAERESIS) == _DIAERESIS:
            diacriticBits &= ~_DIAERESIS
        else:
            diacriticBits |= _DIAERESIS
        diacriticBits &= cancelDiacritics[kDIAERESIS]

    return diacriticBits

def isLegalDiacriticForLetter(letterCode, accentToAdd):
    #match these strings to the arguments in the accelerators
    if accentToAdd == kCIRCUMFLEX:
        if letterCode != ALPHA and letterCode != ETA and letterCode != IOTA and letterCode != UPSILON and letterCode != OMEGA and letterCode != ALPHA_CAP and letterCode != ETA_CAP and letterCode != IOTA_CAP and letterCode != UPSILON_CAP and letterCode != OMEGA_CAP:
            return False
    elif accentToAdd == kMACRON:
        if letterCode != ALPHA and letterCode != IOTA and letterCode != UPSILON and letterCode != ALPHA_CAP and letterCode != IOTA_CAP and letterCode != UPSILON_CAP:
            return False
    elif accentToAdd == kBREVE:
        if letterCode != ALPHA and letterCode != IOTA and letterCode != UPSILON and letterCode != ALPHA_CAP and letterCode != IOTA_CAP and letterCode != UPSILON_CAP:
            return False
    elif accentToAdd == kIOTA_SUBSCRIPT:
        if letterCode != ALPHA and letterCode != ETA and letterCode != OMEGA and letterCode != ALPHA_CAP and letterCode != ETA_CAP and letterCode != OMEGA_CAP:
            return False
    elif accentToAdd == kDIAERESIS:
        if letterCode != IOTA and letterCode != UPSILON and letterCode != IOTA_CAP and letterCode != UPSILON_CAP:
            return False
    return True


#a hash table could save us from looping through all this
#we don't want to analyze via canonical decomposition because PUA characters are not canonical
def analyzePrecomposedLetter(letter):
    for vidx in range(0, NUM_VOWEL_CODES):
        for aidx in range(0, NUM_ACCENT_CODES):
            if letter[0] == letters[vidx][aidx]:
                return (vidx, aidx)
    return (None, None)


def precomposedIndexToBitMask(diacriticIndex, diacriticBits):
    #don't initialize to false here because diacriticMask could have combining accents already set to true
    #make sure this is in order of enum so compiler can optimize switch
    if diacriticIndex == PSILI:
        diacriticBits |= _SMOOTH
    elif diacriticIndex == DASIA:
        diacriticBits |= _ROUGH
    elif diacriticIndex == OXIA:
        diacriticBits |= _ACUTE
    elif diacriticIndex == PSILI_AND_OXIA:
        diacriticBits |= (_SMOOTH | _ACUTE)
    elif diacriticIndex == DASIA_AND_OXIA:
        diacriticBits |= (_ROUGH | _ACUTE)
    elif diacriticIndex == VARIA:
        diacriticBits |= _GRAVE
    elif diacriticIndex == PSILI_AND_VARIA:
        diacriticBits |= (_SMOOTH | _GRAVE)
    elif diacriticIndex == DASIA_AND_VARIA:
        diacriticBits |= (_ROUGH | _GRAVE)
    elif diacriticIndex == PERISPOMENI:
        diacriticBits |= _CIRCUMFLEX
    elif diacriticIndex == PSILI_AND_PERISPOMENI:
        diacriticBits |= (_SMOOTH | _CIRCUMFLEX)
    elif diacriticIndex == DASIA_AND_PERISPOMENI:
        diacriticBits |= (_ROUGH | _CIRCUMFLEX)
    elif diacriticIndex == YPOGEGRAMMENI:
        diacriticBits |= _IOTA_SUB
    elif diacriticIndex == PSILI_AND_YPOGEGRAMMENI:
        diacriticBits |= (_SMOOTH | _IOTA_SUB)
    elif diacriticIndex == DASIA_AND_YPOGEGRAMMENI:
        diacriticBits |= (_ROUGH | _IOTA_SUB)
    elif diacriticIndex == OXIA_AND_YPOGEGRAMMENI:
        diacriticBits |= (_ACUTE | _IOTA_SUB)
    elif diacriticIndex == PSILI_AND_OXIA_AND_YPOGEGRAMMENI:
        diacriticBits |= (_SMOOTH | _ACUTE | _IOTA_SUB)
    elif diacriticIndex == DASIA_AND_OXIA_AND_YPOGEGRAMMENI:
        diacriticBits |= (_ROUGH | _ACUTE | _IOTA_SUB)
    elif diacriticIndex == VARIA_AND_YPOGEGRAMMENI:
        diacriticBits |= (_GRAVE | _IOTA_SUB)
    elif diacriticIndex == PSILI_AND_VARIA_AND_YPOGEGRAMMENI:
        diacriticBits |= (_SMOOTH | _GRAVE | _IOTA_SUB)
    elif diacriticIndex == DASIA_AND_VARIA_AND_YPOGEGRAMMENI:
        diacriticBits |= (_ROUGH | _GRAVE | _IOTA_SUB)
    elif diacriticIndex == PERISPOMENI_AND_YPOGEGRAMMENI:
        diacriticBits |= (_CIRCUMFLEX | _IOTA_SUB)
    elif diacriticIndex == PSILI_AND_PERISPOMENI_AND_YPOGEGRAMMENI:
        diacriticBits |= (_SMOOTH | _CIRCUMFLEX | _IOTA_SUB)
    elif diacriticIndex == DASIA_AND_PERISPOMENI_AND_YPOGEGRAMMENI:
        diacriticBits |= (_ROUGH | _CIRCUMFLEX | _IOTA_SUB)
    elif diacriticIndex == DIALYTIKA:
        diacriticBits |= _DIAERESIS
    elif diacriticIndex == DIALYTIKA_AND_OXIA:
        diacriticBits |= (_DIAERESIS | _ACUTE)
    elif diacriticIndex == DIALYTIKA_AND_VARIA:
        diacriticBits |= (_DIAERESIS | _GRAVE)
    elif diacriticIndex == DIALYTIKA_AND_PERISPOMENON:
        diacriticBits |= (_DIAERESIS | _CIRCUMFLEX)
    elif diacriticIndex == MACRON_PRECOMPOSED:
        diacriticBits |= _MACRON
#ifdef ALLOW_PRIVATE_USE_AREA
    elif diacriticIndex == MACRON_AND_SMOOTH:
        diacriticBits |= (_MACRON | _SMOOTH)
    elif diacriticIndex == MACRON_AND_SMOOTH_AND_ACUTE:
        diacriticBits |= (_MACRON | _SMOOTH | _ACUTE)
    elif diacriticIndex == MACRON_AND_SMOOTH_AND_GRAVE:
        diacriticBits |= (_MACRON | _SMOOTH | _GRAVE)
    elif diacriticIndex == MACRON_AND_ROUGH:
        diacriticBits |= (_MACRON | _ROUGH)
    elif diacriticIndex == MACRON_AND_ROUGH_AND_ACUTE:
        diacriticBits |= (_MACRON | _ROUGH | _ACUTE)
    elif diacriticIndex == MACRON_AND_ROUGH_AND_GRAVE:
        diacriticBits |= (_MACRON | _ROUGH | _GRAVE)
    elif diacriticIndex == MACRON_AND_ACUTE:
        diacriticBits |= (_MACRON | _ACUTE)
    elif diacriticIndex == MACRON_AND_GRAVE:
        diacriticBits |= (_MACRON | _GRAVE)
#endif
    elif diacriticIndex == TONOS: #we conflate tonos and acute
        diacriticBits |= _ACUTE
    return diacriticBits

#returns a tuple (letterIndex, diacriticsBits) or (None,None)
def analyzeLetter(letter):
    #fix me in c version, better here
    diacriticBits = 0

    letterLen = len(letter)
    if letterLen > 1:
        for l in letter: # (int j = 1; j <= MAX_COMBINING && i + j < len; j++)
            if l == COMBINING_ROUGH_BREATHING:
                diacriticBits |= _ROUGH
            elif l == COMBINING_SMOOTH_BREATHING:
                diacriticBits |= _SMOOTH
            elif l == COMBINING_ACUTE:
                diacriticBits |= _ACUTE
            elif l == COMBINING_GRAVE:
                diacriticBits |= _GRAVE
            elif l == COMBINING_CIRCUMFLEX:
                diacriticBits |= _CIRCUMFLEX
            elif l == COMBINING_MACRON:
                diacriticBits |= _MACRON
            elif l == COMBINING_BREVE:
                diacriticBits |= _BREVE
            elif l == COMBINING_IOTA_SUBSCRIPT:
                diacriticBits |= _IOTA_SUB
            elif l == COMBINING_DIAERESIS:
                diacriticBits |= _DIAERESIS
            else:
                continue #continue, not break because first letter is not combining

    (letterIndex, diacriticIndex) = analyzePrecomposedLetter(letter)
    if letterIndex is None:
        return (None, None)
    
    diacriticBits = precomposedIndexToBitMask(diacriticIndex, diacriticBits)

    return (letterIndex, diacriticBits)


def accentLetter(letter, diacritic, vUnicodeMode, bToggleOff):
    try:
        if int(vUnicodeMode) < 0 or int(vUnicodeMode) > 3:
            vUnicodeMode = 0
    except ValueError:
        vUnicodeMode = 0
        
    bAddSpacingDiacriticIfNotLegal = False #for now

    #handle rho 
    rho = '\u03c1'
    rho_with_dasia = '\u1fe5'
    rho_with_psili = '\u1fe4'
    rho_cap = '\u03a1'
    rho_cap_with_dasia = '\u1fec'

    if letter == rho and diacritic == kROUGH_BREATHING:
        return rho_with_dasia
    elif letter == rho_with_dasia and diacritic == kROUGH_BREATHING:
        return rho
    elif letter == rho_cap and diacritic == kROUGH_BREATHING:
        return rho_cap_with_dasia
    elif letter == rho_cap_with_dasia and diacritic == kROUGH_BREATHING:
        return rho_cap
    elif letter == rho_with_psili and diacritic == kROUGH_BREATHING:
        return rho_with_dasia
#ifdef ALLOW_RHO_WITH_PSILI
    elif letter == rho and diacritic == kSMOOTH_BREATHING:
        return rho_with_psili
    elif letter == rho_with_psili and diacritic == kSMOOTH_BREATHING:
        return rho
    elif letter == rho_with_dasia and diacritic == kSMOOTH_BREATHING:
        return rho_with_psili
#endif

    #1. analyze the letter to be accented
    (letterIndex, diacriticBits) = analyzeLetter(letter)
    if letterIndex is None:
        return None

    #2. is it legal to add this diacritic?
    if isLegalDiacriticForLetter(letterIndex, diacritic) == False:
        return None

    #3. add new diacritic to the existing diacritics, making adjustments accordingly
    diacriticBits = updateDiacritics(letterIndex, diacriticBits, diacritic, bToggleOff)

    #4. make and return the new character
    newLetter = makeLetter(letterIndex, diacriticBits, vUnicodeMode)
    if newLetter is None:
        return None
    else:
        return newLetter
        