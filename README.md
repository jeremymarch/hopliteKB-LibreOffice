# HopliteKB-LibreOffice
LibreOffice Extension implementing the Hoplite Polytonic Greek Keyboard

## Features:
* One key per diacritic
* Add diacritics _after_ typing the vowel
* Add diacritics in any order
* Toggle diacritics on/off
* breathings, accents, subscripts, macrons, breves, diaereses: no problem!\*
* (coming soon: choose precombined, precombined with private use area, or combining-only modes)

\* as long as your font supports it.

## Installation:
Zip the contents of the **hoplitekb-ext** folder into a zip file and rename the zip **hoplitekb.oxt**.  Be sure not to include any enclosing folder in the zip file or the extension will fail to load.  From the terminal, these steps can be combined by running **_zip -r ../hoplitekb.oxt \*_** from inside the hoplite-ext folder.  Now from LibreOffice, add the extension by going to Tools -> Extension Manager and clicking Add; select the file hoplitekb.oxt and restart LibreOffice.

## Use:
Now you can add Polytonic Greek diacritics by pressing Control (Command on Mac) and 1-9 to toggle on/off diacritics.  From 1-9 the keys are bound to:
	rough breathing, smooth breathing, acute, grave, circumflex, macron, breve, iota subscript, and diaeresis.
The key bindings can be changed in Accelerators.xcu.

For best results, use a Polytonic Greek font such as: 
* [New Athena Unicode](https://apagreekkeys.org/NAUdownload.html)
* [IFAOGrec Unicode](http://www.ifao.egnet.net/publications/publier/outils-ed/polices/#grec)
