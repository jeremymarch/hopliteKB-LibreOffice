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
from urllib.parse import unquote

# Add current directory to path to import local modules
cmd_folder = os.path.realpath(os.path.abspath
                                  (os.path.split(inspect.getfile
                                                 ( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import hopliteaccent
import optionsdialog

from com.sun.star.task import XJobExecutor

#https://forum.openoffice.org/en/forum/viewtopic.php?t=43492#
from com.sun.star.frame import (XStatusListener,
   XDispatchProvider,
   XDispatch, XControlNotificationListener, FeatureStateEvent)
from com.sun.star.lang import XInitialization, XServiceInfo

#from unicodedata import normalize #another way we could do some of this, but won't work for PUA 

# PRECOMPOSED_MODE = 0
# PRECOMPOSED_WITH_PUA_MODE = 1
# COMBINING_ONLY_MODE = 2
# PRECOMPOSED_HC_MODE = 3
vUnicodeMode = hopliteaccent.PRECOMPOSED_MODE #default

def setUnicodeMode(mode):
    global vUnicodeMode
    vUnicodeMode = mode

# def get_extension_path(ctx):
#     srv = ctx.getByName("/singletons/com.sun.star.deployment.PackageInformationProvider")
#     extPath = unquote(srv.getPackageLocation("com.philolog.hoplitekb")) #unquote file url, was giving %02 for spaces
#     extPath = extPath.split("://")[1] #remove "file://"
#     return extPath

# def getSettingsPath(ctx):
#     path = get_extension_path(ctx)
#     path = os.path.dirname(path) 
#     return path + "/hoplite.txt"

class HopliteKB( unohelper.Base, XJobExecutor ):
    def __init__( self, ctx ):
        self.ctx = ctx
        # if vUnicodeMode < 0:
        #     self.initializeOptionsOnce()
        
    def trigger( self, args ):

        try:
            if args is None or len(args) < 1:
                return

            # if normalize("NFC", u"α") == normalize("NFC", u"α"):
            #     a = "abc"
            # else:
            #     a = "bcd"
            #text.insertString( cursor, a, 0 ) #print exception

            desktop = self.ctx.ServiceManager.createInstanceWithContext( "com.sun.star.frame.Desktop", self.ctx )

            doc = desktop.getCurrentComponent()
            text = doc.Text
            cursor = text.createTextCursor()

            #text.insertString( cursor, "ABC: 1 :DEF", 0 ) #print exception
            #self.writeSettings(1)

            #we use a global and not class member because class is recreated for each call
            # global vUnicodeMode #global because we are modifying it below
            # if args == "setmodeprecomposing":
            #     vUnicodeMode = hopliteaccent.PRECOMPOSED_MODE
            #     self.writeSettings(vUnicodeMode)
            #     #text.insertString( cursor, "prec ", 0 ) #print exception
            #     return
            # elif args == "setmodepua":
            #     vUnicodeMode = hopliteaccent.PRECOMPOSED_WITH_PUA_MODE
            #     self.writeSettings(vUnicodeMode)
            #     #text.insertString( cursor, "pua ", 0 ) #print exception
            #     return
            # elif args == "setmodecombining":
            #     vUnicodeMode = hopliteaccent.COMBINING_ONLY_MODE
            #     self.writeSettings(vUnicodeMode)
            #     #text.insertString( cursor, "combining ", 0 ) #print exception
            #     return
            if args == "acute":
                diacriticToAdd = hopliteaccent.kACUTE
            elif args == "circumflex":
                diacriticToAdd = hopliteaccent.kCIRCUMFLEX
            elif args == "grave":
                diacriticToAdd = hopliteaccent.kGRAVE
            elif args == "macron":
                diacriticToAdd = hopliteaccent.kMACRON
            elif args == "rough":
                diacriticToAdd = hopliteaccent.kROUGH_BREATHING
            elif args == "smooth":
                diacriticToAdd = hopliteaccent.kSMOOTH_BREATHING
            elif args == "iotasub":
                diacriticToAdd = hopliteaccent.kIOTA_SUBSCRIPT
            elif args == "diaeresis":
                diacriticToAdd = hopliteaccent.kDIAERESIS
            elif args == "breve":
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


# IMPL_NAME = "com.philolog.hoplitekbTest"


# class Dispatcher(unohelper.Base, XDispatch, XControlNotificationListener):
#    def __init__(self, frame, ctx):
#       self.frame = frame
#       self.ctx = ctx
#       #self.state = False
#       self.listener = None

#    # XDispatch
#    def dispatch(self, url, args):
#       #self.state = not self.state

#       ev = self.create_simple_event(url, True)
#       self.listener.statusChanged(ev)
      
#       self.setMode(url.Path)

#       paths = ["setmodeprecomposing", "setmodepua", "setmodecombining"]
#       paths.remove(url.Path)

#       #unset other modes
#       for p in paths:
#         url.Path = p
#         url.Main = "com.philolog.hoplitekb:" + p
#         url.Complete = "com.philolog.hoplitekb:" + p
#         ev2 = self.create_simple_event(url, False)
#         self.listener.statusChanged(ev2)
   
#    def addStatusListener(self, listener, url):
#       self.listener = listener
   
#    def removeStatusListener(self, listener, url): pass
   
#    # XControlNotificationListener
#    def controlEvent(self, ev): pass
   
#    def create_simple_event(self, url, state, enabled=True):
#       return FeatureStateEvent(self, url, "", enabled, False, state)
   
   
#    def setMode(self, mode):
#      global vUnicodeMode
#      if mode == "setmodeprecomposing":
#         vUnicodeMode = hopliteaccent.PRECOMPOSED_MODE
#      elif mode == "setmodepua":
#         vUnicodeMode = hopliteaccent.PRECOMPOSED_WITH_PUA_MODE
#      elif mode == "setmodecombining":   
#         vUnicodeMode = hopliteaccent.COMBINING_ONLY_MODE
#      self.writeSettings(vUnicodeMode)  
    
#       # if self.frame:
#       #    controller = self.frame.getController()
#       #    doc = controller.getModel()
#       #    if doc.supportsService("com.sun.star.text.TextDocument"):
#       #       doc.getText().setString("New state: %s" % url)

#    def writeSettings(self, vUnicodeMode):
#         path = getSettingsPath(self.ctx) 
#         file = open(path, "w+") 
#         file.write( str(vUnicodeMode) ) 
#         file.close() 


# class HopliteKBPh(unohelper.Base, XInitialization, XDispatchProvider, XServiceInfo):
#    def __init__(self, ctx, *args):
#       self.frame = None
#       self.ctx = ctx
   
#    # XInitialization
#    def initialize(self, args):
#       if len(args) > 0:
#          self.frame = args[0]
#       global vUnicodeMode
#       vUnicodeMode = self.readSettings()
      

#    def readSettings(self):
#       path = getSettingsPath(self.ctx) 
#       file = open(path, "r") 
#       mode = file.read(1) #read one char
#       file.close()
#       if mode == hopliteaccent.PRECOMPOSED_MODE or mode == hopliteaccent.PRECOMPOSED_WITH_PUA_MODE or mode == hopliteaccent.COMBINING_ONLY_MODE:
#          return mode
#       else:
#          return hopliteaccent.PRECOMPOSED_MODE #default to precomposed
   
#    # XDispatchProvider
#    def queryDispatch(self, url, name, flag):
#       dispatch = None
#       if url.Protocol == "com.philolog.hoplitekb:":
#          try:
#             dispatch = Dispatcher(self.frame, self.ctx)
#          except Exception as e:
#             print(e)
#       return dispatch
   
#    def queryDispatches(self, descs):
#       pass
   
#    # XServiceInfo
#    def supportsService(self, name):
#       return (name == "com.sun.star.frame.ProtocolHandler")
#    def getImplementationName(self):
#       return IMPL_NAME
#    def getSupportedServiceNames(self):
#       return ("com.sun.star.frame.ProtocolHandler",)

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
        
g_ImplementationHelper = unohelper.ImplementationHelper()

# g_ImplementationHelper.addImplementation(
#    HopliteKBPh,
#     "com.philolog.hoplitekbTest",
#    ("com.sun.star.frame.ProtocolHandler",),)


IMPLE_NAME = "com.philolog.hoplitekb"
SERVICE_NAME = "com.philolog.hoplitekb.Settings"
def create(ctx, *args):    
    # pythopathフォルダのモジュールの取得。
    return optionsdialog.create(ctx, *args, imple_name=IMPLE_NAME, service_name=SERVICE_NAME, on_options_changed=setUnicodeMode)

g_ImplementationHelper.addImplementation(create, IMPLE_NAME, (SERVICE_NAME,),)

g_ImplementationHelper.addImplementation(
        HopliteKB,
        "com.philolog.hoplitekb.kb",
        ("com.sun.star.task.Job",),)
