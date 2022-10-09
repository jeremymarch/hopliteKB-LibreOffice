#!
# -*- coding: utf-8 -*-
import unohelper
from com.sun.star.awt import XContainerWindowEventHandler
from com.sun.star.lang import XServiceInfo
from com.sun.star.awt import XActionListener
from com.sun.star.beans import PropertyValue

# from com.sun.star.awt.PosSize import POSSIZE  # ピクセル単位でコントロールの座標を指定するときにPosSizeキーの値に使う。
#import traceback

def create(ctx, *args, imple_name, service_name, on_options_changed, reload_diacritics_keys):
	global IMPLE_NAME
	global SERVICE_NAME
	IMPLE_NAME = imple_name
	SERVICE_NAME = service_name
	dh = DilaogHandler(ctx, on_options_changed, reload_diacritics_keys, *args)
	return dh

class DilaogHandler(unohelper.Base, XServiceInfo, XContainerWindowEventHandler):  # UNOコンポーネントにするクラス。
	METHODNAME = "external_event"  # 変更できない。
	def __init__(self, ctx, on_options_changed, reload_diacritics_keys, *args):
		self.ctx = ctx
		self.on_options_changed = on_options_changed
		self.reload_diacritics_keys = reload_diacritics_keys
		self.smgr = ctx.getServiceManager()
		self.readConfig, self.writeConfig = createConfigAccessor(ctx, self.smgr, "/com.philolog.hoplitekb.ExtensionData/Leaves/HKBSettingsNode")  # config.xcsに定義していあるコンポーネントデータノードへのパス。
		self.cfgnames = "Width", "Height", "UnicodeMode", "roughKey", "smoothKey", "acuteKey", "graveKey", "circumflexKey", "macronKey", "breveKey", "iotaKey", "diaeresisKey"
		self.defaults = self.readConfig("Defaults/Width", "Defaults/Height", "Defaults/UnicodeMode", "Defaults/roughKey", "Defaults/smoothKey", "Defaults/acuteKey", "Defaults/graveKey", "Defaults/circumflexKey", "Defaults/macronKey", "Defaults/breveKey", "Defaults/iotaKey", "Defaults/diaeresisKey")

	# XContainerWindowEventHandler
	def callHandlerMethod(self, dialog, eventname, methodname):  # ブーリアンを返す必要あり。dialogはUnoControlDialog。 eventnameは文字列initialize, ok, backのいずれか。methodnameは文字列external_event。
		if methodname==self.METHODNAME:  # Falseのときがありうる?
			try:
				if eventname=="initialize":  # オプションダイアログがアクティブになった時
					maxwidth, maxheight, umode, roughKey, smoothKey, acuteKey, graveKey, circumflexKey, macronKey, breveKey, iotaKey, diaeresisKey  = self.readConfig(*self.cfgnames)  # コンポーネントデータノードの値を取得。取得した値は文字列。
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
					#dialog.getControl("debug").getModel().Text = roughKey + " ciao ciao " + smoothKey + " ciao ciao " + acuteKey + " ciao ciao " + graveKey + " ciao ciao " + circumflexKey + " ciao ciao " + macronKey + " ciao ciao " + breveKey + " ciao ciao " + iotaKey + " ciao ciao " + diaeresisKey 

				elif eventname=="ok":  # OKボタンが押された時
					if dialog.getControl("PrecomposedPUAOption").getModel().State == True:
						umode = "PrecomposedPUA"
						self.on_options_changed(1) #hopliteaccent.PRECOMPOSED_WITH_PUA_MODE
					elif dialog.getControl("CombiningOption").getModel().State == True:
						umode = "CombiningOnly"
						self.on_options_changed(2) #hopliteaccent.COMBINING_ONLY_MODE
					else:
						umode = "Precomposed"
						self.on_options_changed(0) #hopliteaccent.PRECOMPOSED_MODE

					roughKey_new = dialog.getControl("roughKey").getModel().Text
					smoothKey_new = dialog.getControl("smoothKey").getModel().Text
					acuteKey_new = dialog.getControl("acuteKey").getModel().Text
					graveKey_new = dialog.getControl("graveKey").getModel().Text
					circumflexKey_new = dialog.getControl("circumflexKey").getModel().Text
					macronKey_new = dialog.getControl("macronKey").getModel().Text
					breveKey_new = dialog.getControl("breveKey").getModel().Text
					iotaKey_new = dialog.getControl("iotaKey").getModel().Text
					diaeresisKey_new = dialog.getControl("diaeresisKey").getModel().Text
						
					self.writeConfig(self.cfgnames, (str("300"), str("300"), str(umode), str(roughKey_new), str(smoothKey_new), str(acuteKey_new), str(graveKey_new), str(circumflexKey_new), str(macronKey_new), str(breveKey_new), str(iotaKey_new), str(diaeresisKey_new)))  # 取得した値を文字列にしてコンポーネントデータノードに保存。
					self.reload_diacritics_keys()
				elif eventname=="back":  # 元に戻すボタンが押された時
					maxwidth, maxheight, umode, roughKey, smoothKey, acuteKey, graveKey, circumflexKey, macronKey, breveKey, iotaKey, diaeresisKey  = self.readConfig(*self.cfgnames)
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

			except:
				#traceback.print_exc()  # トレースバックはimport pydevd; pydevd.settrace(stdoutToServer=True, stderrToServer=True)でブレークして取得できるようになる。
				return False
		return True

	def getSupportedMethodNames(self):
		return (self.METHODNAME,)  # これも決め打ち。

	# XServiceInfo
	def getImplementationName(self):
		return IMPLE_NAME
	def supportsService(self, name):
		return name == SERVICE_NAME
	def getSupportedServiceNames(self):
		return (SERVICE_NAME,)


def createConfigAccessor(ctx, smgr, rootpath):  # コンポーネントデータノードへのアクセス。
	cp = smgr.createInstanceWithContext("com.sun.star.configuration.ConfigurationProvider", ctx)
	node = PropertyValue(Name="nodepath", Value=rootpath)
	root = cp.createInstanceWithArguments("com.sun.star.configuration.ConfigurationUpdateAccess", (node,))
	def readConfig(*args):  # 値の取得。整数か文字列かブーリアンのいずれか。コンポーネントスキーマノードの設定に依存。
		if len(args)==1:  # 引数の数が1つのとき
			return root.getHierarchicalPropertyValue(*args)
		elif len(args)>1:  # 引数の数が2つ以上のとき
			return root.getHierarchicalPropertyValues(args)
	def writeConfig(names, values):  # 値の書き込み。整数か文字列かブーリアンのいずれか。コンポーネントスキーマノードの設定に依存。
		try:
			if isinstance(names, tuple):  # 引数がタプルのとき
				root.setHierarchicalPropertyValues(names, values)
			else:
				root.setHierarchicalPropertyValue(names, values)
			root.commitChanges()  # 変更値の書き込み。
		except:
			pass
			#traceback.print_exc()
	return readConfig, writeConfig
