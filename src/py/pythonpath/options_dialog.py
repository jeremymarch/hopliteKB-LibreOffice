# -*- coding: utf-8 -*-
import unohelper
from com.sun.star.awt import XContainerWindowEventHandler
from com.sun.star.lang import XServiceInfo
from com.sun.star.beans import PropertyValue

# import traceback
import hoplite_accent


def create(ctx, *args, imple_name, service_name, on_options_changed, reload_diacritics_keys):
    """Creates the options dialog handler.

    on_options_changed() and reload_diacritics_keys() are functions which are passed in from hoplitekb.py

    """

    global IMPLE_NAME
    global SERVICE_NAME
    IMPLE_NAME = imple_name
    SERVICE_NAME = service_name
    dh = DialogHandler(ctx, on_options_changed, reload_diacritics_keys, *args)
    return dh


class DialogHandler(unohelper.Base, XServiceInfo, XContainerWindowEventHandler):
    METHODNAME = "external_event"

    def __init__(self, ctx, on_options_changed, reload_diacritics_keys, *args):
        self.ctx = ctx
        self.on_options_changed = on_options_changed
        self.reload_diacritics_keys = reload_diacritics_keys
        self.smgr = ctx.getServiceManager()
        self.readConfig, self.writeConfig = createConfigAccessor(ctx, self.smgr, "/com.philolog.hoplitekb.ExtensionData/Leaves/HKBSettingsNode")
        self.cfgnames = "Width", "Height", "UnicodeMode", "roughKey", "smoothKey", "acuteKey", "graveKey", "circumflexKey", "macronKey", "breveKey", "iotaKey", "diaeresisKey"
        self.defaults = self.readConfig("Defaults/Width", "Defaults/Height", "Defaults/UnicodeMode", "Defaults/roughKey", "Defaults/smoothKey", "Defaults/acuteKey", "Defaults/graveKey", "Defaults/circumflexKey", "Defaults/macronKey", "Defaults/breveKey", "Defaults/iotaKey", "Defaults/diaeresisKey")

    # XContainerWindowEventHandler
    def callHandlerMethod(self, dialog, eventname, methodname):
        """Handle initialize and button press events from the options dialog."""

        if methodname == self.METHODNAME:
            try:
                if eventname == "initialize":
                    maxwidth, maxheight, umode, roughKey, smoothKey, acuteKey, graveKey, circumflexKey, macronKey, breveKey, iotaKey, diaeresisKey = self.readConfig(*self.cfgnames)
                    umode = umode or self.defaults[2]
                    maxwidth = maxwidth or self.defaults[0]
                    maxheight = maxheight or self.defaults[1]
                    roughKey = roughKey or self.defaults[3]
                    smoothKey = smoothKey or self.defaults[4]
                    acuteKey = acuteKey or self.defaults[5]
                    graveKey = graveKey or self.defaults[6]
                    circumflexKey = circumflexKey or self.defaults[7]
                    macronKey = macronKey or self.defaults[8]
                    breveKey = breveKey or self.defaults[9]
                    iotaKey = iotaKey or self.defaults[10]
                    diaeresisKey = diaeresisKey or self.defaults[11]

                    if umode == "PrecomposedPUA":
                        dialog.getControl("PrecomposedOption").getModel().State = False
                        dialog.getControl("PrecomposedPUAOption").getModel().State = True
                        dialog.getControl("CombiningOption").getModel().State = False
                    elif umode == "CombiningOnly":
                        dialog.getControl("PrecomposedOption").getModel().State = False
                        dialog.getControl("PrecomposedPUAOption").getModel().State = False
                        dialog.getControl("CombiningOption").getModel().State = True
                    else:
                        dialog.getControl("PrecomposedOption").getModel().State = True
                        dialog.getControl("PrecomposedPUAOption").getModel().State = False
                        dialog.getControl("CombiningOption").getModel().State = False

                    dialog.getControl("roughKey").getModel().Text = roughKey
                    dialog.getControl("smoothKey").getModel().Text = smoothKey
                    dialog.getControl("acuteKey").getModel().Text = acuteKey
                    dialog.getControl("graveKey").getModel().Text = graveKey
                    dialog.getControl("circumflexKey").getModel().Text = circumflexKey
                    dialog.getControl("macronKey").getModel().Text = macronKey
                    dialog.getControl("breveKey").getModel().Text = breveKey
                    dialog.getControl("iotaKey").getModel().Text = iotaKey
                    dialog.getControl("diaeresisKey").getModel().Text = diaeresisKey
                    # dialog.getControl("debug").getModel().Text = roughKey + " ciao ciao " + smoothKey + " ciao ciao " + acuteKey + " ciao ciao " + graveKey + " ciao ciao " + circumflexKey + " ciao ciao " + macronKey + " ciao ciao " + breveKey + " ciao ciao " + iotaKey + " ciao ciao " + diaeresisKey

                elif eventname == "ok":
                    if dialog.getControl("PrecomposedPUAOption").getModel().State == 1:  # == 1 instead of True to satisfy flake8
                        umode = "PrecomposedPUA"
                        self.on_options_changed(hoplite_accent.UnicodeMode.PRECOMPOSED_WITH_PUA)  # 1
                    elif dialog.getControl("CombiningOption").getModel().State == 1:  # == 1 instead of True to satisfy flake8
                        umode = "CombiningOnly"
                        self.on_options_changed(hoplite_accent.UnicodeMode.COMBINING_ONLY)  # 2
                    else:
                        umode = "Precomposed"
                        self.on_options_changed(hoplite_accent.UnicodeMode.PRECOMPOSED)  # 0

                    roughKey_new = dialog.getControl("roughKey").getModel().Text
                    smoothKey_new = dialog.getControl("smoothKey").getModel().Text
                    acuteKey_new = dialog.getControl("acuteKey").getModel().Text
                    graveKey_new = dialog.getControl("graveKey").getModel().Text
                    circumflexKey_new = dialog.getControl("circumflexKey").getModel().Text
                    macronKey_new = dialog.getControl("macronKey").getModel().Text
                    breveKey_new = dialog.getControl("breveKey").getModel().Text
                    iotaKey_new = dialog.getControl("iotaKey").getModel().Text
                    diaeresisKey_new = dialog.getControl("diaeresisKey").getModel().Text

                    self.writeConfig(self.cfgnames, (str("300"), str("300"), str(umode), str(roughKey_new), str(smoothKey_new), str(acuteKey_new), str(graveKey_new), str(circumflexKey_new), str(macronKey_new), str(breveKey_new), str(iotaKey_new), str(diaeresisKey_new)))
                    self.reload_diacritics_keys()
                elif eventname == "back":
                    maxwidth, maxheight, umode, roughKey, smoothKey, acuteKey, graveKey, circumflexKey, macronKey, breveKey, iotaKey, diaeresisKey = self.readConfig(*self.cfgnames)
                    umode = umode or self.defaults[2]
                    maxwidth = maxwidth or self.defaults[0]
                    maxheight = maxheight or self.defaults[1]
                    roughKey = roughKey or self.defaults[3]
                    smoothKey = smoothKey or self.defaults[4]
                    acuteKey = acuteKey or self.defaults[5]
                    graveKey = graveKey or self.defaults[6]
                    circumflexKey = circumflexKey or self.defaults[7]
                    macronKey = macronKey or self.defaults[8]
                    breveKey = breveKey or self.defaults[9]
                    iotaKey = iotaKey or self.defaults[10]
                    diaeresisKey = diaeresisKey or self.defaults[11]
                    if umode == "PrecomposedPUA":
                        dialog.getControl("PrecomposedOption").getModel().State = False
                        dialog.getControl("PrecomposedPUAOption").getModel().State = True
                        dialog.getControl("CombiningOption").getModel().State = False
                    elif umode == "CombiningOnly":
                        dialog.getControl("PrecomposedOption").getModel().State = False
                        dialog.getControl("PrecomposedPUAOption").getModel().State = False
                        dialog.getControl("CombiningOption").getModel().State = True
                    else:
                        dialog.getControl("PrecomposedOption").getModel().State = True
                        dialog.getControl("PrecomposedPUAOption").getModel().State = False
                        dialog.getControl("CombiningOption").getModel().State = False

                    dialog.getControl("roughKey").getModel().Text = roughKey
                    dialog.getControl("smoothKey").getModel().Text = smoothKey
                    dialog.getControl("acuteKey").getModel().Text = acuteKey
                    dialog.getControl("graveKey").getModel().Text = graveKey
                    dialog.getControl("circumflexKey").getModel().Text = circumflexKey
                    dialog.getControl("macronKey").getModel().Text = macronKey
                    dialog.getControl("breveKey").getModel().Text = breveKey
                    dialog.getControl("iotaKey").getModel().Text = iotaKey
                    dialog.getControl("diaeresisKey").getModel().Text = diaeresisKey

            except Exception as e:
                if False:
                    print(e)
                # traceback.print_exc()
                return False
        return True

    def getSupportedMethodNames(self):
        return (self.METHODNAME,)

    # XServiceInfo
    def getImplementationName(self):
        return IMPLE_NAME

    def supportsService(self, name):
        return name == SERVICE_NAME

    def getSupportedServiceNames(self):
        return (SERVICE_NAME,)


def createConfigAccessor(ctx, smgr, rootpath):
    cp = smgr.createInstanceWithContext("com.sun.star.configuration.ConfigurationProvider", ctx)
    node = PropertyValue(Name="nodepath", Value=rootpath)
    root = cp.createInstanceWithArguments("com.sun.star.configuration.ConfigurationUpdateAccess", (node,))

    def readConfig(*args):
        if len(args) == 1:
            return root.getHierarchicalPropertyValue(*args)
        elif len(args) > 1:
            return root.getHierarchicalPropertyValues(args)

    def writeConfig(names, values):
        try:
            if isinstance(names, tuple):
                root.setHierarchicalPropertyValues(names, values)
            else:
                root.setHierarchicalPropertyValue(names, values)
            root.commitChanges()
        except Exception as e:
            if False:
                print(e)
            pass
            # traceback.print_exc()
    return readConfig, writeConfig
