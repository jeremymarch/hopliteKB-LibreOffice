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

#toggle button modeled after: https://forum.openoffice.org/en/forum/viewtopic.php?p=200474#p200474

import sys
import os
import inspect
import uno
import unohelper
from com.sun.star.lang import XServiceInfo
from com.sun.star.frame import XDispatchProvider
from com.sun.star.frame import XDispatch
from com.sun.star.awt import XKeyHandler

from com.sun.star.frame import (XStatusListener, 
	XDispatchProvider, 
	XDispatch, XControlNotificationListener, FeatureStateEvent)
from com.sun.star.lang import XInitialization, XServiceInfo

#import gettext
#_ = gettext.gettext

# Add current directory to path to import local modules
cmd_folder = os.path.realpath(os.path.abspath
                                  (os.path.split(inspect.getfile
                                                 ( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import hopliteaccent
import optionsdialog

ImplementationName = "com.philolog.hoplitekb.ProtocolHandler"
ServiceName = "com.sun.star.frame.ProtocolHandler"
Protocol = "com.philolog.hoplitekb:"


def getTextRange(controller):
    xSelectionSupplier = controller

    xIndexAccess = xSelectionSupplier.getSelection()
    count = xIndexAccess.getCount()

    # don't handle multiple selections
    if (count != 1):
        return None

    textrange = xIndexAccess.getByIndex(0)

    if (len(textrange.getString()) == 0):
        return textrange
    else:
        return None


def insertString(ctx, string):
    smgr = ctx.getServiceManager()
    desktop = smgr.createInstanceWithContext(
            "com.sun.star.frame.Desktop", ctx)
    doc = desktop.getCurrentComponent()
    controller = doc.getCurrentController()
    textrange = getTextRange(controller)
    if (textrange is None):
        return

    try:
        timestamp = string
        if timestamp is not None:
            textrange.setString(timestamp)
    except Exception:
        pass

#set default
vUnicodeMode = hopliteaccent.PRECOMPOSED_MODE 

def setUnicodeMode(mode):
    global vUnicodeMode
    vUnicodeMode = mode

transliterateLetters = {
  "a": "α",
  "b": "β",
  "g": "γ",
  "d": "δ",
  "e": "ε",
  "z": "ζ",
  "h": "η",
  "u": "θ",
  "i": "ι",
  "k": "κ",
  "l": "λ",
  "m": "μ",
  "n": "ν",
  "j": "ξ",
  "o": "ο",
  "p": "π",
  "r": "ρ",
  "s": "σ",
  "w": "ς",
  "t": "τ",
  "y": "υ",
  "f": "φ",
  "x": "χ",
  "c": "ψ",
  "v": "ω",
  "A": "Α",
  "B": "Β",
  "G": "Γ",
  "D": "Δ",
  "E": "Ε",
  "Z": "Ζ",
  "H": "Η",
  "U": "Θ",
  "I": "Ι",
  "K": "Λ",
  "L": "Λ",
  "M": "Μ",
  "N": "Ν",
  "J": "Ξ",
  "O": "Ο",
  "P": "Π",
  "R": "Ρ",
  "S": "Σ",
  "T": "Τ",
  "Y": "Υ",
  "F": "Φ",
  "X": "Χ",
  "C": "Ψ",
  "V": "Ω"
}

def transliterate(s):
    return transliterateLetters.get(s)

class Dispatcher(unohelper.Base, XDispatch, XControlNotificationListener):
    def __init__(self, parent):
        self.state = False
        self.listener = None
        self.parent = parent
	
	# XDispatch
    def dispatch(self, url, args):
        self.state = not self.state
        ev = self.create_simple_event(url, self.state)
        self.listener.statusChanged(ev)

        self.toggle_action()
	
    def addStatusListener(self, listener, url):
        self.listener = listener
	
    def removeStatusListener(self, listener, url): pass
	
	# XControlNotificationListener
    def controlEvent(self, ev): pass
	
    def create_simple_event(self, url, state, enabled=True):
        return FeatureStateEvent(self, url, "", enabled, False, state) #this shades the button to indicate toggled state
	
    def toggle_action(self):
        if self.state == False:
            self.parent.stopkb()
        else:
            self.parent.startkb()

class KeyHandler(unohelper.Base, XKeyHandler):

    def __init__(self, parent, ctx):
        self.parent = parent
        self.ctx = ctx

    def keyPressed(self, oEvent):
        letter = oEvent.KeyChar.value
        if letter.isnumeric():
            self.parent.toggleDiacritic(letter)
            return True
        a = transliterate(letter)
        if a != None:
            insertString(self.ctx, a)
            return True
        return False

    def keyReleased(self, oEvent):
        return False

    def disposing(self, source):
        pass

class ToolbarHandler(unohelper.Base, XServiceInfo,
                     XDispatchProvider, XDispatch):

    def __init__(self, ctx):
        self.ctx = ctx
        self.key_handler = KeyHandler(self, self.ctx)

    def toggleDiacritic(self, args):

        try:
            if args is None or len(args) < 1:
                return

            desktop = self.ctx.ServiceManager.createInstanceWithContext( "com.sun.star.frame.Desktop", self.ctx )

            doc = desktop.getCurrentComponent()
            text = doc.Text
            cursor = text.createTextCursor()

            if args == "3":#"acute":
                diacriticToAdd = hopliteaccent.kACUTE
            elif args == "5":#"circumflex":
                diacriticToAdd = hopliteaccent.kCIRCUMFLEX
            elif args == "4":#"grave":
                diacriticToAdd = hopliteaccent.kGRAVE
            elif args == "6":#"macron":
                diacriticToAdd = hopliteaccent.kMACRON
            elif args == "1":#"rough":
                diacriticToAdd = hopliteaccent.kROUGH_BREATHING
            elif args == "2":#"smooth":
                diacriticToAdd = hopliteaccent.kSMOOTH_BREATHING
            elif args == "8":#"iotasub":
                diacriticToAdd = hopliteaccent.kIOTA_SUBSCRIPT
            elif args == "9":#"diaeresis":
                diacriticToAdd = hopliteaccent.kDIAERESIS
            elif args == "7":#"breve":
                diacriticToAdd = hopliteaccent.kBREVE
            else:
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
                newLetter = hopliteaccent.accentLetter(letterToAccent, diacriticToAdd, vUnicodeMode, True)
                if newLetter is not None:
                    xWordCursor.setString(newLetter)

        except Exception as e:
            #text.insertString( cursor, str(e), 0 ) #print exception
            #print('hello python to console')
            pass

    # XServiceInfo
    def supportsService(self, name):
        return (name == ServiceName)

    def getImplementationName(self):
        return ImplementationName

    def getSupportedServiceNames(self):
        return (ServiceName,)

    # XDispatchProvider
    def queryDispatch(self, url, name, flag):
            dispatch = None
            if url.Protocol == Protocol:
                try:
                    dispatch = Dispatcher(self)
                except Exception as e:
                    print(e)
            return dispatch

    def queryDispatches(self, requests):
        #never called
        dispatches = \
            [self.queryDispatch(r.FeatureURL, r.FrameName, r.SearchFlags)
                for r in requests]
        return dispatches

    def startkb(self):
        smgr = self.ctx.getServiceManager()
        self.desktop = smgr.createInstanceWithContext(
            "com.sun.star.frame.Desktop", self.ctx)
        doc = self.desktop.getCurrentComponent()
        controller = doc.getCurrentController()
        #controller.removeKeyHandler(self.key_handler) #be sure there is only
        controller.addKeyHandler(self.key_handler)

    def stopkb(self):
        smgr = self.ctx.getServiceManager()
        self.desktop = smgr.createInstanceWithContext(
            "com.sun.star.frame.Desktop", self.ctx)
        doc = self.desktop.getCurrentComponent()
        controller = doc.getCurrentController()
        controller.removeKeyHandler(self.key_handler)

    # XDispatch
    # def dispatch(self, url, args):
    #     if url.Protocol == Protocol:
    #         if url.Path == "open":
    #             if self.kbOn:
    #                 self.stopkb()
    #             else:
    #                 self.startkb()

# uno implementation
g_ImplementationHelper = unohelper.ImplementationHelper()

g_ImplementationHelper.addImplementation(
    ToolbarHandler,
    ImplementationName,
    (ServiceName,),)


# Settings
def initializeOptionsOnce():
    ctx = uno.getComponentContext()
    smgr = ctx.getServiceManager()
    readConfig, writeConfig = optionsdialog.createConfigAccessor(ctx, smgr, "/com.philolog.hoplitekb.ExtensionData/Leaves/HKBSettingsNode")
    defaults = readConfig("Defaults/Width", "Defaults/Height", "Defaults/UnicodeMode")
    #set current value
    cfgnames = "Width", "Height", "UnicodeMode"
    maxwidth, maxheight, umode = readConfig(*cfgnames)
    umode = umode or defaults[2]
    if umode == "PrecomposedPUA":
        setUnicodeMode(1)
    elif umode == "CombiningOnly":
        setUnicodeMode(2)
    else:
        setUnicodeMode(0)

initializeOptionsOnce()

IMPLE_NAME = "com.philolog.hoplitekb.OptionsDialog"
SERVICE_NAME = "com.philolog.hoplitekb.OptionsDialog"
def create(ctx, *args):
    return optionsdialog.create(ctx, *args, imple_name=IMPLE_NAME, service_name=SERVICE_NAME, on_options_changed=setUnicodeMode)

g_ImplementationHelper.addImplementation(create, IMPLE_NAME, (SERVICE_NAME,),)
