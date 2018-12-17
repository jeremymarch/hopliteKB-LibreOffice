# -*- coding: utf-8 -*-

#
#  hoplitekb.py
#  HopliteKB-LibreOffice
#
#  Created by Jeremy March on 12/06/18.
#  Copyright (c) 2018 Jeremy March. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import os
import sys
import inspect
import uno
import unohelper

# Add current directory to path to import local modules
cmd_folder = os.path.realpath(os.path.abspath
                                  (os.path.split(inspect.getfile
                                                 ( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import hopliteaccent

from com.sun.star.task import XJobExecutor
#from unicodedata import normalize #another way we could do some of this, but won't work for PUA 

vUnicodeMode = hopliteaccent.PRECOMPOSED_WITH_PUA_MODE #default


class HopliteKB( unohelper.Base, XJobExecutor ):
    def __init__( self, ctx ):
        self.ctx = ctx
        # PRECOMPOSED_MODE = 0
        # PRECOMPOSED_WITH_PUA_MODE = 1
        # COMBINING_ONLY_MODE = 2
        # PRECOMPOSED_HC_MODE = 3
        
    def trigger( self, args ):

        try:
            if args is None or len(args) < 1:
                return

            # if normalize("NFC", u"α") == normalize("NFC", u"α"):
            #     a = "abc"
            # else:
            #     a = "bcd"
            #text.insertString( cursor, a, 0 ) #print exception

            diacriticToAdd = args

            desktop = self.ctx.ServiceManager.createInstanceWithContext( "com.sun.star.frame.Desktop", self.ctx )

            doc = desktop.getCurrentComponent()
            text = doc.Text
            cursor = text.createTextCursor()

            #we use a global and not class member because class is recreated for each call
            global vUnicodeMode #global because we are modifying it below
            if args == "setmodeprecomposing":
                vUnicodeMode = hopliteaccent.PRECOMPOSED_MODE
                #text.insertString( cursor, "prec ", 0 ) #print exception
                return
            elif args == "setmodepua":
                vUnicodeMode = hopliteaccent.PRECOMPOSED_WITH_PUA_MODE
                #text.insertString( cursor, "pua ", 0 ) #print exception
                return
            elif args == "setmodecombining":
                vUnicodeMode = hopliteaccent.COMBINING_ONLY_MODE
                #text.insertString( cursor, "combining ", 0 ) #print exception
                return

            xIndexAccess = doc.getCurrentSelection()
            xTextRange = xIndexAccess.getByIndex(0) #just the first selection
            xText = xTextRange.getText()
            xWordCursor = xText.createTextCursorByRange(xTextRange)
            xWordCursor.collapseToEnd()

            #go right to be sure the cursor we don't miss any combining chars, in case cursor is between them and letter; max 6
            n = 0
            for i in range(0, 6):
                xWordCursor.goRight(1, True)
                s = xWordCursor.getString()
                if s is not None and len(s) > 0 and s[-1] not in hopliteaccent.combiningAccents:
                    xWordCursor.collapseToStart() #roll back one
                    break
                n = n + 1
                xWordCursor.collapseToEnd() #go one by one

            #leave right fixed and go left until no more combining chars
            for j in range(0, 6 + n):
                xWordCursor.goLeft(1, True)
                s = xWordCursor.getString()
                if s is not None and len(s) > 0 and s[0] not in hopliteaccent.combiningAccents: #when != "a" this puts us one further past the comb. chars.
                    break

            #get letter with any following combining chars, we decide what to do inside accentLetter
            letterToAccent = xWordCursor.getString()
            if letterToAccent is not None and len(letterToAccent) > 0:
                newLetter = hopliteaccent.accentLetter(letterToAccent, diacriticToAdd, vUnicodeMode)
                if newLetter is not None:
                    xWordCursor.setString(newLetter)

        except Exception as e:
            text.insertString( cursor, str(e), 0 ) #print exception
            #print('hello python to console')
            pass

        
g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(
        HopliteKB,
        "com.philolog.hoplitekb",
        ("com.sun.star.task.Job",),)
