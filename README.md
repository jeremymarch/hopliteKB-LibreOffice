# HopliteKB-LibreOffice
LibreOffice Extension implementing the Hoplite Polytonic Greek Keyboard

Type polytonic Greek diacritics with ease.  

For LibreOffice 5.2 and up on Linux, Mac, and Windows.

## Features:
* One key per diacritic
* Add diacritics _after_ typing the vowel
* Add diacritics in any order
* Toggle diacritics on/off
* Breathings, accents, subscripts, macrons, breves, diaereses: no problem!\*
* Choose precomposed, precomposed with private use area, or combining-only modes.

\* as long as your font supports it.

For best results, use a polytonic Greek font such as: 
* [New Athena Unicode](https://apagreekkeys.org/NAUdownload.html)
* [IFAOGrec Unicode](http://www.ifao.egnet.net/publications/publier/outils-ed/polices/#grec)

## Installation:
The extension is contained in the file hoplitekb.oxt.  Download this file from the [**release**](https://github.com/jeremymarch/HopliteKB-LibreOffice/releases) tab above.  From LibreOffice, add the extension by going to Tools -> Extension Manager and clicking Add; select the file hoplitekb.oxt and restart LibreOffice.

To build the extension from source code, clone this repository.  Run the build.sh script to build the extension.  Install hoplitekb.oxt in LibreOffice as above.

## Use:
Toggle on the extension by pressing the icon installed in the toolbar. The letters a-z and A-Z will be automatically transliterated into Greek characters. To add diacritics, after typing a vowel, press a key 1-9 to toggle on/off diacritics.  The 1-9 keys, by default, are bound to: 
1. rough breathing 
2. smooth breathing
3. acute
4. grave
5. circumflex
6. macron
7. breve
8. iota subscript
9. diaeresis

The default key bindings can be changed in the extension preferences.

## Options:
The options menu can be accessed on Mac from LibreOffice -> Preferences -> LibreOffice Writer -> Hoplite Keyboard.  On Linux and Windows it can be accessed from Tools -> Options -> LibreOffice Writer -> Hoplite Keyboard.  On all platforms it can also be accessed from Tools -> Extension Manager; then select the extension and click the Options button.  

From the options menu you can select the Unicode mode.  
* **Precomposed** mode uses precomposed characters when possible, falling back to combining diacritics for combinations where a precomposed character does not exist in the Unicode standard.  
* **Precomposed with PUA** (Private Use Area) mode is the same, but also uses the precomposed characters from the non-standard Private Use Area.  These characters are not standard Unicode, but are supported by some fonts such as New Athena Unicode and IFAOGrec Unicode.  
* **Combining-only** mode uses combining diacritics to type decomposed characters.  Few fonts handle combining diacritics well at this point; New Athena Unicode is currently the best.  

There is a detailed discussion of these differences [here](https://apagreekkeys.org/technicalDetails.html).

From the options menu you can also define different key bindings for adding diacritics.

## Why a LibreOffice extension?  Why not offer this functionality system-wide?
The Linux, Mac, and Windows operating systems do not provide the keyboard with the information necessary to toggle on/off diacritics.  The Hoplite Keyboard started on [iOS](https://github.com/jeremymarch/HopliteKB-iOS) and [Android](https://github.com/jeremymarch/HopliteKB-Android) where this information *is* provided to the keyboard.  So for Linux, Mac, and Windows the only way to implement this is inside applications.

## To Do:
* The PUA characters documented [here](https://apagreekkeys.org/technicalDetails.html) are only partially implemented (only the macron combinations on α, ι, and υ).  
* Some uncommon characters are currently blocked, e.g. circumflex over short vowels, etc.
* analyzePrecomposedLetter() is inefficient.  Use unicodedata to canonically decompose or create own look up table.


