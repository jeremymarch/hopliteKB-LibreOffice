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
# pythonpath is added to sys.path by LibreOffice uno
import hoplite_accent
import options_dialog

ImplementationName = "com.philolog.hoplitekb.ProtocolHandler"
ServiceName = "com.sun.star.frame.ProtocolHandler"
Protocol = "com.philolog.hoplitekb:"


def get_text_range(controller):
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


# insert a string at the selected text range
def insert_string(ctx, string):
    smgr = ctx.getServiceManager()
    desktop = smgr.createInstanceWithContext(
            "com.sun.star.frame.Desktop", ctx)
    doc = desktop.getCurrentComponent()
    controller = doc.getCurrentController()
    textrange = get_text_range(controller)
    if (textrange is None):
        return

    try:
        if string is not None:
            textrange.setString(string)
    except Exception:
        pass


# set default
unicode_mode = hoplite_accent.UnicodeMode.PRECOMPOSED
diacritics_keys = []


def set_diacritic_keys(val):
    global diacritics_keys
    diacritics_keys = val


def set_unicode_mode(mode):
    global unicode_mode
    unicode_mode = mode


transliterate_letters = {
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
    return transliterate_letters.get(s)


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
        if letter in diacritics_keys:
            self.parent.toggle_diacritic(letter)
            return True
        a = transliterate(letter)
        if a is not None:
            insert_string(self.ctx, a)
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

    def toggle_diacritic(self, args):
        try:
            if args is None or len(args) < 1:
                return

            desktop = self.ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", self.ctx)

            doc = desktop.getCurrentComponent()
            # text = doc.Text
            # cursor = text.createTextCursor()

            if args == diacritics_keys[0]:  # "1": #"rough":
                diacritic_to_add = hoplite_accent.Diacritic.ROUGH_BREATHING
            elif args == diacritics_keys[1]:  # "2": #"smooth":
                diacritic_to_add = hoplite_accent.Diacritic.SMOOTH_BREATHING
            elif args == diacritics_keys[2]:  # "3": #"acute":
                diacritic_to_add = hoplite_accent.Diacritic.ACUTE
            elif args == diacritics_keys[3]:  # "4": #"grave":
                diacritic_to_add = hoplite_accent.Diacritic.GRAVE
            elif args == diacritics_keys[4]:  # "5": #"circumflex":
                diacritic_to_add = hoplite_accent.Diacritic.CIRCUMFLEX
            elif args == diacritics_keys[5]:  # "6": #"macron":
                diacritic_to_add = hoplite_accent.Diacritic.MACRON
            elif args == diacritics_keys[6]:  # "7": #"breve":
                diacritic_to_add = hoplite_accent.Diacritic.BREVE
            elif args == diacritics_keys[7]:  # "8": #"iotasub":
                diacritic_to_add = hoplite_accent.Diacritic.IOTA_SUBSCRIPT
            elif args == diacritics_keys[8]:  # "9": #"diaeresis":
                diacritic_to_add = hoplite_accent.Diacritic.DIAERESIS
            else:
                return

            xIndexAccess = doc.getCurrentSelection()
            xTextRange = xIndexAccess.getByIndex(0)  # just the first selection
            xText = xTextRange.getText()
            xWordCursor = xText.createTextCursorByRange(xTextRange)
            xWordCursor.collapseToEnd()

            # go right to be sure the cursor we don't miss any combining chars, in case cursor is between a diacritic and the letter; max 6
            n = 0
            for i in range(0, 6):
                xWordCursor.goRight(1, True)
                s = xWordCursor.getString()
                if s is not None and len(s) > 0 and s[-1] not in hoplite_accent.combining_diacritics:
                    xWordCursor.collapseToStart()  # roll back one
                    break
                n = n + 1
                xWordCursor.collapseToEnd()  # go one by one

            # leave right fixed and go left until no more combining chars
            for j in range(0, 6 + n):
                xWordCursor.goLeft(1, True)
                s = xWordCursor.getString()
                if s is not None and len(s) > 0 and s[0] not in hoplite_accent.combining_diacritics:  # when != "a" this puts us one further past the comb. chars.
                    break

            # get letter with any following combining chars, we decide what to do inside accent_letter
            letter_to_accent = xWordCursor.getString()
            if letter_to_accent is not None and len(letter_to_accent) > 0:
                new_letter = hoplite_accent.accent_letter(letter_to_accent, diacritic_to_add, unicode_mode, True)
                if new_letter is not None:
                    xWordCursor.setString(new_letter)

        except Exception as e:
            if False:
                print(e)
            # text.insert_string( cursor, str(e), 0 ) #print exception
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
                # insert_string(self.ctx, str(e))
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
def initialize_options_once():
    ctx = uno.getComponentContext()
    smgr = ctx.getServiceManager()
    readConfig, writeConfig = options_dialog.createConfigAccessor(ctx, smgr, "/com.philolog.hoplitekb.ExtensionData/Leaves/HKBSettingsNode")
    defaults = readConfig("Defaults/Width", "Defaults/Height", "Defaults/UnicodeMode")
    # set current value
    cfgnames = "Width", "Height", "UnicodeMode"
    maxwidth, maxheight, umode = readConfig(*cfgnames)
    umode = umode or defaults[2]
    if umode == "PrecomposedPUA":
        set_unicode_mode(hoplite_accent.UnicodeMode.PRECOMPOSED_WITH_PUA)  # 1
    elif umode == "CombiningOnly":
        set_unicode_mode(hoplite_accent.UnicodeMode.COMBINING_ONLY)  # 2
    else:
        set_unicode_mode(hoplite_accent.UnicodeMode.PRECOMPOSED)  # 0


def load_diacritic_keys():
    ctx = uno.getComponentContext()
    smgr = ctx.getServiceManager()
    readConfig, writeConfig = options_dialog.createConfigAccessor(ctx, smgr, "/com.philolog.hoplitekb.ExtensionData/Leaves/HKBSettingsNode")
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
    set_diacritic_keys([roughKey, smoothKey, acuteKey, graveKey, circumflexKey, macronKey, breveKey, iotaKey, diaeresisKey])


initialize_options_once()
load_diacritic_keys()

IMPLE_NAME = "com.philolog.hoplitekb.OptionsDialog"
SERVICE_NAME = "com.philolog.hoplitekb.OptionsDialog"


# set_unicode_mode() and load_diacritic_keys() are passed into options_dialog.py here
def create(ctx, *args):
    return options_dialog.create(ctx, *args, imple_name=IMPLE_NAME, service_name=SERVICE_NAME, on_options_changed=set_unicode_mode, reload_diacritics_keys=load_diacritic_keys)


g_ImplementationHelper.addImplementation(create, IMPLE_NAME, (SERVICE_NAME,),)
