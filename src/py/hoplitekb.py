# -*- coding: utf-8 -*-
#
#  hoplitekb.py
#  HopliteKB-LibreOffice
#
#  Created by Jeremy March on 12/06/18.
#  Copyright (c) 2018-2022 Jeremy March. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

# toggle button modeled after: https://forum.openoffice.org/en/forum/viewtopic.php?p=200474#p200474

import uno
import unohelper
from com.sun.star.lang import XServiceInfo
from com.sun.star.awt import XKeyHandler

from com.sun.star.frame import (XDispatchProvider,
                                XDispatch, XControlNotificationListener, FeatureStateEvent)

# put these two modules in subdirectory called pythonpath
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

    # if (len(textrange.getString()) == 0):
    #     return textrange
    # else:
    #     return None
    return textrange  # allow ranges with length greater than zero: will replace whole range with character


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


# set default
vUnicodeMode = hopliteaccent.UnicodeMode.PRECOMPOSED
diacriticsKeys = []


def setDiacriticsKeys(val):
    global diacriticsKeys
    diacriticsKeys = val


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
  "K": "Κ",
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
  "V": "Ω",
  "?": ";",
  ";": "·"
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
        self.listener.statusChanged(ev)  # this shades the button to indicate toggled state
        self.toggle_action()

    def addStatusListener(self, listener, url):
        self.listener = listener

    def removeStatusListener(self, listener, url): pass

    # XControlNotificationListener
    def controlEvent(self, ev): pass

    def create_simple_event(self, url, state, enabled=True):
        return FeatureStateEvent(self, url, "", enabled, False, state)

    def toggle_action(self):
        if self.state is False:
            self.parent.stopkb()
        else:
            self.parent.startkb()


class KeyHandler(unohelper.Base, XKeyHandler):

    def __init__(self, parent, ctx):
        self.parent = parent
        self.ctx = ctx

    def keyPressed(self, oEvent):
        # do not interfere with modified keys except shift
        # 1 shift                SHIFT
        # 2 control/command      MOD1
        # 4 alt                  MOD2
        # 8 control on macOS     MOD3
        if oEvent.Modifiers != 0 and oEvent.Modifiers != 1:
            return False
        letter = oEvent.KeyChar.value
        if letter in diacriticsKeys:
            self.parent.toggleDiacritic(letter)
            return True
        a = transliterate(letter)
        if a is not None:
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

            desktop = self.ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", self.ctx)

            doc = desktop.getCurrentComponent()
            # text = doc.Text
            # cursor = text.createTextCursor()

            if args == diacriticsKeys[2]:  # "3": #"acute":
                diacriticToAdd = hopliteaccent.DiacriticKey.ACUTE
            elif args == diacriticsKeys[4]:  # "5": #"circumflex":
                diacriticToAdd = hopliteaccent.DiacriticKey.CIRCUMFLEX
            elif args == diacriticsKeys[3]:  # "4": #"grave":
                diacriticToAdd = hopliteaccent.DiacriticKey.GRAVE
            elif args == diacriticsKeys[5]:  # "6": #"macron":
                diacriticToAdd = hopliteaccent.DiacriticKey.MACRON
            elif args == diacriticsKeys[0]:  # "1": #"rough":
                diacriticToAdd = hopliteaccent.DiacriticKey.ROUGH_BREATHING
            elif args == diacriticsKeys[1]:  # "2": #"smooth":
                diacriticToAdd = hopliteaccent.DiacriticKey.SMOOTH_BREATHING
            elif args == diacriticsKeys[7]:  # "8": #"iotasub":
                diacriticToAdd = hopliteaccent.DiacriticKey.IOTA_SUBSCRIPT
            elif args == diacriticsKeys[8]:  # "9": #"diaeresis":
                diacriticToAdd = hopliteaccent.DiacriticKey.DIAERESIS
            elif args == diacriticsKeys[6]:  # "7": #"breve":
                diacriticToAdd = hopliteaccent.DiacriticKey.BREVE
            else:
                return

            xIndexAccess = doc.getCurrentSelection()
            xTextRange = xIndexAccess.getByIndex(0)  # just the first selection
            xText = xTextRange.getText()
            xWordCursor = xText.createTextCursorByRange(xTextRange)
            xWordCursor.collapseToEnd()

            # go right to be sure the cursor we don't miss any combining chars, in case cursor is between them and letter; max 6
            n = 0
            for i in range(0, 6):
                xWordCursor.goRight(1, True)
                s = xWordCursor.getString()
                if s is not None and len(s) > 0 and s[-1] not in hopliteaccent.combining_accents:
                    xWordCursor.collapseToStart()  # roll back one
                    break
                n = n + 1
                xWordCursor.collapseToEnd()  # go one by one

            # leave right fixed and go left until no more combining chars
            for j in range(0, 6 + n):
                xWordCursor.goLeft(1, True)
                s = xWordCursor.getString()
                if s is not None and len(s) > 0 and s[0] not in hopliteaccent.combining_accents:  # when != "a" this puts us one further past the comb. chars.
                    break

            # get letter with any following combining chars, we decide what to do inside accent_letter
            letterToAccent = xWordCursor.getString()
            if letterToAccent is not None and len(letterToAccent) > 0:
                newLetter = hopliteaccent.accent_letter(letterToAccent, diacriticToAdd, vUnicodeMode, True)
                if newLetter is not None:
                    xWordCursor.setString(newLetter)

        except Exception as e:
            if False:
                print(e)
            # text.insertString( cursor, str(e), 0 ) #print exception
            # print('hello python to console')
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
                # insertString(self.ctx, str(e))
        return dispatch

    def queryDispatches(self, requests):
        # never called
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
        # controller.removeKeyHandler(self.key_handler) #be sure there is only
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
    # set current value
    cfgnames = "Width", "Height", "UnicodeMode"
    maxwidth, maxheight, umode = readConfig(*cfgnames)
    umode = umode or defaults[2]
    if umode == "PrecomposedPUA":
        setUnicodeMode(hopliteaccent.UnicodeMode.PRECOMPOSED_WITH_PUA)  # 1
    elif umode == "CombiningOnly":
        setUnicodeMode(hopliteaccent.UnicodeMode.COMBINING_ONLY)  # 2
    else:
        setUnicodeMode(hopliteaccent.UnicodeMode.PRECOMPOSED)  # 0


def loadDiacriticsKeys():
    ctx = uno.getComponentContext()
    smgr = ctx.getServiceManager()
    readConfig, writeConfig = optionsdialog.createConfigAccessor(ctx, smgr, "/com.philolog.hoplitekb.ExtensionData/Leaves/HKBSettingsNode")
    defaults = readConfig("Defaults/Width", "Defaults/Height", "Defaults/UnicodeMode", "Defaults/roughKey", "Defaults/smoothKey", "Defaults/acuteKey", "Defaults/graveKey", "Defaults/circumflexKey", "Defaults/macronKey", "Defaults/breveKey", "Defaults/iotaKey", "Defaults/diaeresisKey")
    # set current value
    cfgnames = "Width", "Height", "UnicodeMode", "roughKey", "smoothKey", "acuteKey", "graveKey", "circumflexKey", "macronKey", "breveKey", "iotaKey", "diaeresisKey"
    maxwidth, maxheight, umode, roughKey, smoothKey, acuteKey, graveKey, circumflexKey, macronKey, breveKey, iotaKey, diaeresisKey = readConfig(*cfgnames)
    roughKey = roughKey or defaults[3]
    smoothKey = smoothKey or defaults[4]
    acuteKey = acuteKey or defaults[5]
    graveKey = graveKey or defaults[6]
    circumflexKey = circumflexKey or defaults[7]
    macronKey = macronKey or defaults[8]
    breveKey = breveKey or defaults[9]
    iotaKey = iotaKey or defaults[10]
    diaeresisKey = diaeresisKey or defaults[11]
    setDiacriticsKeys([roughKey, smoothKey, acuteKey, graveKey, circumflexKey, macronKey, breveKey, iotaKey, diaeresisKey])


initializeOptionsOnce()
loadDiacriticsKeys()

IMPLE_NAME = "com.philolog.hoplitekb.OptionsDialog"
SERVICE_NAME = "com.philolog.hoplitekb.OptionsDialog"


def create(ctx, *args):
    return optionsdialog.create(ctx, *args, imple_name=IMPLE_NAME, service_name=SERVICE_NAME, on_options_changed=setUnicodeMode, reload_diacritics_keys=loadDiacriticsKeys)


g_ImplementationHelper.addImplementation(create, IMPLE_NAME, (SERVICE_NAME,),)
