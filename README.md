# HopliteKB-LibreOffice
LibreOffice Extension implementing the Hoplite Polytonic Greek Keyboard

Type polytonic Greek diacritics with ease.

## Features:
* One key per diacritic
* Add diacritics _after_ typing the vowel
* Add diacritics in any order
* Toggle diacritics on/off
* breathings, accents, subscripts, macrons, breves, diaereses: no problem!\*
* (coming soon: choose precombined, precombined with private use area, or combining-only modes)

\* as long as your font supports it.

For best results, use a Polytonic Greek font such as: 
* [New Athena Unicode](https://apagreekkeys.org/NAUdownload.html)
* [IFAOGrec Unicode](http://www.ifao.egnet.net/publications/publier/outils-ed/polices/#grec)

## Installation:
The extension is contained in the file hoplitekb.oxt.  Download this file from the **release** tab above.  From LibreOffice, add the extension by going to Tools -> Extension Manager and clicking Add; select the file hoplitekb.oxt and restart LibreOffice.

To create the extension from source code, clone this repository.  Now zip the contents of the **hoplitekb-ext** folder into a zip file and rename the zip **hoplitekb.oxt**.  Be sure not to include the enclosing folder itself, i.e. hoplitekb-ext, in the zip file or the extension will fail to load.  From the terminal, these steps can be easily combined by running **_zip -r ../hoplitekb.oxt \*_** from inside the hoplite-ext folder.  Install hoplitekb.oxt in LibreOffice as above.

## Use:
Add polytonic Greek diacritics by first typing a Greek vowel (or rho).  Next, while holding Control (Command on Mac), press a key 1-9 to toggle on/off diacritics.  Respectively, the 1-9 keys are bound to: rough breathing, smooth breathing, acute, grave, circumflex, macron, breve, iota subscript, and diaeresis.  The key bindings can be changed in the file Accelerators.xcu; then rezip the extension and reinstall.

## Why a LibreOffice extension?  Why not offer this functionality system-wide?:
The Windows, Mac, and Linux opererating systems do not provide the keyboard with the information necessary to toggle on/off diacritics.  The Hoplite Keyboard started on iOS and Android where this information *is* provided to the keyboard.  So for Windows, Mac, and Linux the only way to implement this is inside applications. Hence a LibreOffice extension.

