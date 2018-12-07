# -*- coding: utf-8 -*-
# make extension from repo directory: zip -r ../python_example.oxt * 

#get char to right
#if combining, move right until not combining char
#select left until not combining
#if it's a vowel or rho, this is our string.

#these two are the main basis of this extension
#https://forum.openoffice.org/en/forum/viewtopic.php?t=70633
#https://wiki.openoffice.org/wiki/PyUNO_samples

#https://ask.libreoffice.org/en/question/12614/python-macro-to-insert-text-at-gui-cursor-position/
#https://stackoverflow.com/questions/49728663/enumerate-fieldmarks-in-a-libreoffice-document#49735882

#https://github.com/slgobinath/libreoffice-code-highlighter/blob/master/codehighlighter/python/highlight.py
#https://github.com/kelsa-pi/unodit

#com sun star text XTextCursor : https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1text_1_1XTextCursor.html
#keyboard stuff: https://github.com/XRoemer/Organon/blob/master/source/py/shortcuts.py

#chart: https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1frame_1_1XModel.html#a1ee3a9fe564e0757381e23ef1a401eef

#iterate by char (java) https://stackoverflow.com/questions/38124658/how-to-navigate-through-each-character-in-open-office

#useful c++ guide: https://wiki.openoffice.org/wiki/Writer/API/Overview#The_XTextCursor_Interface
#and this: https://wiki.openoffice.org/wiki/Uno/Cpp/Tutorials/Introduction_to_Cpp_Uno

#https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1text_1_1XTextCursor.html

#we'll need to go one by one and then save end loc in a range, then create new range if vowel is found
#this is because we can't shrink the range once we find the right end of the combining chars.

import uno
import unohelper

from com.sun.star.task import XJobExecutor

_MACRON     = 1 << 0
_SMOOTH     = 1 << 1
_ROUGH      = 1 << 2
_ACUTE      = 1 << 3
_GRAVE      = 1 << 4
_CIRCUMFLEX = 1 << 5
_IOTA_SUB   = 1 << 6
_DIAERESIS  = 1 << 7
_BREVE      = 1 << 8 

COMBINING_GRAVE                 = b'\\u0300'
COMBINING_ACUTE                 = b'\\u0301'
COMBINING_CIRCUMFLEX            = b'\\u0342' #0x0302
COMBINING_MACRON                = b'\\u0304'
COMBINING_BREVE                 = b'\\u0306'
COMBINING_DIAERESIS             = b'\\u0308'
COMBINING_SMOOTH_BREATHING      = b'\\u0313'
COMBINING_ROUGH_BREATHING       = b'\\u0314'
COMBINING_IOTA_SUBSCRIPT        = b'\\u0342'
# EM_DASH                         0x2014
# LEFT_PARENTHESIS                0x0028
# RIGHT_PARENTHESIS               0x0029
# SPACE                           0x0020
# EN_DASH                         0x2013
# HYPHEN                          0x2010
# COMMA                           0x002C

# gamma is a comb char, delta is a vowel
#gamma = b'\\u03b3' #just for testing
combiningAccents = [ COMBINING_MACRON, COMBINING_BREVE, COMBINING_DIAERESIS, COMBINING_ROUGH_BREATHING, COMBINING_SMOOTH_BREATHING, COMBINING_ACUTE, COMBINING_GRAVE, COMBINING_CIRCUMFLEX, COMBINING_IOTA_SUBSCRIPT ];


vowels = 14
accents = 37

letters = [ [ b'\\u03B1', b'\\u1F00', b'\\u1F01', b'\\u1F71', b'\\u1F04', b'\\u1F05', b'\\u1F70', b'\\u1F02', b'\\u1F03', b'\\u1FB6', b'\\u1F06', b'\\u1F07', b'\\u1FB3', b'\\u1F80', b'\\u1F81', b'\\u1FB4', b'\\u1F84', b'\\u1F85', b'\\u1FB2', b'\\u1F82', b'\\u1F83', b'\\u1FB7', b'\\u1F86', b'\\u1F87', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u1FB1', b'\\uEB04', b'\\uEB07', b'\\uEAF3', b'\\uEB05', b'\\uEB09', b'\\uEAF4', b'\\uEB00', b'\\uEAF0' ], 
[ b'\\u03B5', b'\\u1F10', b'\\u1F11', b'\\u1F73', b'\\u1F14', b'\\u1F15', b'\\u1F72', b'\\u1F12', b'\\u1F13', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000' ], 
[ b'\\u03B7', b'\\u1F20', b'\\u1F21', b'\\u1F75', b'\\u1F24', b'\\u1F25', b'\\u1F74', b'\\u1F22', b'\\u1F23', b'\\u1FC6', b'\\u1F26', b'\\u1F27', b'\\u1FC3', b'\\u1F90', b'\\u1F91', b'\\u1FC4', b'\\u1F94', b'\\u1F95', b'\\u1FC2', b'\\u1F92', b'\\u1F93', b'\\u1FC7', b'\\u1F96', b'\\u1F97', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000' ], 
[ b'\\u03B9', b'\\u1F30', b'\\u1F31', b'\\u1F77', b'\\u1F34', b'\\u1F35', b'\\u1F76', b'\\u1F32', b'\\u1F33', b'\\u1FD6', b'\\u1F36', b'\\u1F37', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u03CA', b'\\u1FD3', b'\\u1FD2', b'\\u1FD7', b'\\u1FD1', b'\\uEB3C', b'\\uEB3D', b'\\uEB54', b'\\uEB3E', b'\\uEB3F', b'\\uEB55', b'\\uEB39', b'\\uEB38' ], 
[ b'\\u03BF', b'\\u1F40', b'\\u1F41', b'\\u1F79', b'\\u1F44', b'\\u1F45', b'\\u1F78', b'\\u1F42', b'\\u1F43', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000' ], 
[ b'\\u03C5', b'\\u1F50', b'\\u1F51', b'\\u1F7B', b'\\u1F54', b'\\u1F55', b'\\u1F7A', b'\\u1F52', b'\\u1F53', b'\\u1FE6', b'\\u1F56', b'\\u1F57', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u03CB', b'\\u1FE3', b'\\u1FE2', b'\\u1FE7', b'\\u1FE1', b'\\uEB7D', b'\\uEB7F', b'\\uEB71', b'\\uEB7E', b'\\uEB80', b'\\uEB75', b'\\uEB7A', b'\\uEB6F' ], 
[ b'\\u03C9', b'\\u1F60', b'\\u1F61', b'\\u1F7D', b'\\u1F64', b'\\u1F65', b'\\u1F7C', b'\\u1F62', b'\\u1F63', b'\\u1FF6', b'\\u1F66', b'\\u1F67', b'\\u1FF3', b'\\u1FA0', b'\\u1FA1', b'\\u1FF4', b'\\u1FA4', b'\\u1FA5', b'\\u1FF2', b'\\u1FA2', b'\\u1FA3', b'\\u1FF7', b'\\u1FA6', b'\\u1FA7', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000' ], 
[ b'\\u0391', b'\\u1F08', b'\\u1F09', b'\\u1FBB', b'\\u1F0C', b'\\u1F0D', b'\\u1FBA', b'\\u1F0A', b'\\u1F0B', b'\\u0000', b'\\u1F0E', b'\\u1F0F', b'\\u1FBC', b'\\u1F88', b'\\u1F89', b'\\u0000', b'\\u1F8C', b'\\u1F8D', b'\\u0000', b'\\u1F8A', b'\\u1F8B', b'\\u0000', b'\\u1F8E', b'\\u1F8F', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u1FB9', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000' ], 
[ b'\\u0395', b'\\u1F18', b'\\u1F19', b'\\u1FC9', b'\\u1F1C', b'\\u1F1D', b'\\u1FC8', b'\\u1F1A', b'\\u1F1B', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000' ], 
[ b'\\u0397', b'\\u1F28', b'\\u1F29', b'\\u1FCB', b'\\u1F2C', b'\\u1F2D', b'\\u1FCA', b'\\u1F2A', b'\\u1F2B', b'\\u0000', b'\\u1F2E', b'\\u1F2F', b'\\u1FCC', b'\\u1F98', b'\\u1F99', b'\\u0000', b'\\u1F9C', b'\\u1F9D', b'\\u0000', b'\\u1F9A', b'\\u1F9B', b'\\u0000', b'\\u1F9E', b'\\u1F9F', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000' ], 
[ b'\\u0399', b'\\u1F38', b'\\u1F39', b'\\u1FDB', b'\\u1F3C', b'\\u1F3D', b'\\u1FDA', b'\\u1F3A', b'\\u1F3B', b'\\u0000', b'\\u1F3E', b'\\u1F3F', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u03AA', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u1FD9', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000' ], 
[ b'\\u039F', b'\\u1F48', b'\\u1F49', b'\\u1FF9', b'\\u1F4C', b'\\u1F4D', b'\\u1FF8', b'\\u1F4A', b'\\u1F4B', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000' ], 
[ b'\\u03A5', b'\\u0000', b'\\u1F59', b'\\u1FEB', b'\\u0000', b'\\u1F5D', b'\\u1FEA', b'\\u0000', b'\\u1F5B', b'\\u0000', b'\\u0000', b'\\u1F5F', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u03AB', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u1FE9', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000' ],
[ b'\\u03A9', b'\\u1F68', b'\\u1F69', b'\\u1FFB', b'\\u1F6C', b'\\u1F6D', b'\\u1FFA', b'\\u1F6A', b'\\u1F6B', b'\\u0000', b'\\u1F6E', b'\\u1F6F', b'\\u1FFC', b'\\u1FA8', b'\\u1FA9', b'\\u0000', b'\\u1FAC', b'\\u1FAD', b'\\u0000', b'\\u1FAA', b'\\u1FAB', b'\\u0000', b'\\u1FAE', b'\\u1FAF', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000', b'\\u0000' ] ];


def analyzePrecomposedLetter(letter, letterCodeAndBitMask):
    for vidx in range(0, vowels):
        for aidx in range(0, accents):
            if letter[0].encode("unicode_escape") == letters[vidx][aidx]:
                letterCodeAndBitMask[0] = vidx
                return aidx
    return None


def precomposedIndexToBitMask(precomposedIndex, letterCodeAndBitMask):
    return 0

def analyzeLetter(letter, letterCodeAndBitMask):
    #fix me in c version, better done here
    letterLen = len(letter)
    if letterLen > 1:
        for l in letter: # (int j = 1; j <= MAX_COMBINING && i + j < len; j++)
            if l == COMBINING_ROUGH_BREATHING:
                letterCodeAndBitMask[1] |= _ROUGH
            elif l == COMBINING_SMOOTH_BREATHING:
                letterCodeAndBitMask[1] |= _SMOOTH
            elif l == COMBINING_ACUTE:
                letterCodeAndBitMask[1] |= _ACUTE
            elif l == COMBINING_GRAVE:
                letterCodeAndBitMask[1] |= _GRAVE
            elif l == COMBINING_CIRCUMFLEX:
                letterCodeAndBitMask[1] |= _CIRCUMFLEX;
            elif l == COMBINING_MACRON:
                letterCodeAndBitMask[1] |= _MACRON
            elif l == COMBINING_BREVE:
                letterCodeAndBitMask[1] |= _BREVE
            elif l == COMBINING_IOTA_SUBSCRIPT:
                letterCodeAndBitMask[1] |= _IOTA_SUB
            elif l == COMBINING_DIAERESIS:
                letterCodeAndBitMask[1] |= _DIAERESIS
            else:
                continue

    precomposedIndex = analyzePrecomposedLetter(letter, letterCodeAndBitMask)
    if precomposedIndex is None:
        return None
    
    precomposedIndexToBitMask(precomposedIndex, letterCodeAndBitMask)

    return letterCodeAndBitMask #why return it, it's a ref variable?

def accentLetter(letter, diacritic):
    bToggleOff = True
    bAddSpacingDiacriticIfNotLegal = False #for now
    vUnicodeMode = 0 #0 for precomposed, 1 for precomposed with pua, 2 for combining-only, 3 for legacy hc challenge mode

    #handle rho

    #letters
    letterCodeAndBitMask = [0,0] #list so we can mutate the members
    analyzeLetter(letter, letterCodeAndBitMask)

    if letter == "ά":
        return "α"
    elif letter == "α":
        return "ά"
    else:
        return None

class Example( unohelper.Base, XJobExecutor ):
    def __init__( self, ctx ):
        self.ctx = ctx    

    def trigger( self, args ):

        try:
            if args is None or len(args) < 1:
                return

            diacriticToAdd = args

            desktop = self.ctx.ServiceManager.createInstanceWithContext( "com.sun.star.frame.Desktop", self.ctx )
 
            doc = desktop.getCurrentComponent()
            text = doc.Text;
            cursor = text.createTextCursor();

            xIndexAccess = doc.getCurrentSelection();
            xTextRange = xIndexAccess.getByIndex(0); #just the first selection
            xText = xTextRange.getText();
            xWordCursor = xText.createTextCursorByRange(xTextRange);
            xWordCursor.collapseToEnd();

            #go right to be sure the cursor we don't miss any combining chars, in case cursor is between them and letter; max 6
            n = 0
            for i in range(0, 6):
                xWordCursor.goRight(1, True);
                s = xWordCursor.getString();
                if s is not None and len(s) > 0 and s[-1].encode("unicode_escape") not in combiningAccents:
                    xWordCursor.collapseToStart(); #roll back one
                    break;
                n = n + 1;
                xWordCursor.collapseToEnd(); #go one by one

            #leave right fixed and go left until no more combining chars
            for j in range(0, 6 + n):
                xWordCursor.goLeft(1, True);
                s = xWordCursor.getString();
                if s is not None and len(s) > 0 and s[0].encode("unicode_escape") not in combiningAccents: #when != "a" this puts us one further past the comb. chars.
                    break;

            #get letter with any following combining chars, we decide what to do inside accentLetter
            letterToAccent = xWordCursor.getString();
            if letterToAccent is not None and len(letterToAccent) > 0:
                newLetter = accentLetter(letterToAccent, diacriticToAdd)
                if newLetter is not None:
                    xWordCursor.setString(newLetter);

        except Exception as e:
            text.insertString( cursor, str(e), 0 ) #print exception
            #print('hello python to console')
            pass

        
g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(
        Example,
        "simple.example.identifier",
        ("com.sun.star.task.Job",),)
