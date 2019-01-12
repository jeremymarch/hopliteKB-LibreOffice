#!
# -*- coding: utf-8 -*-
import unohelper
from com.sun.star.awt import XContainerWindowEventHandler
from com.sun.star.lang import XServiceInfo
from com.sun.star.awt import XActionListener
from com.sun.star.beans import PropertyValue
# from com.sun.star.awt.PosSize import POSSIZE  # ピクセル単位でコントロールの座標を指定するときにPosSizeキーの値に使う。
#import traceback

def create(ctx, *args, imple_name, service_name):
	global IMPLE_NAME
	global SERVICE_NAME
	IMPLE_NAME = imple_name
	SERVICE_NAME = service_name
	return DilaogHandler(ctx, *args)

class DilaogHandler(unohelper.Base, XServiceInfo, XContainerWindowEventHandler):  # UNOコンポーネントにするクラス。
	METHODNAME = "external_event"  # 変更できない。
	def __init__(self, ctx, *args):
		self.ctx = ctx
		self.smgr = ctx.getServiceManager()
		self.readConfig, self.writeConfig = createConfigAccessor(ctx, self.smgr, "/com.philolog.hoplitekb.ExtensionData/Leaves/HKBSettingsNode")  # config.xcsに定義していあるコンポーネントデータノードへのパス。
		self.cfgnames = "Width", "Height", "UnicodeMode"
		self.defaults = self.readConfig("Defaults/Width", "Defaults/Height", "Defaults/UnicodeMode")

	# XContainerWindowEventHandler
	def callHandlerMethod(self, dialog, eventname, methodname):  # ブーリアンを返す必要あり。dialogはUnoControlDialog。 eventnameは文字列initialize, ok, backのいずれか。methodnameは文字列external_event。
		if methodname==self.METHODNAME:  # Falseのときがありうる?
			try:
				if eventname=="initialize":  # オプションダイアログがアクティブになった時
					maxwidth, maxheight, umode = self.readConfig(*self.cfgnames)  # コンポーネントデータノードの値を取得。取得した値は文字列。
					umode = umode or self.defaults[2]
					maxwidth = maxwidth or self.defaults[0]
					maxheight = maxheight or self.defaults[1]
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

				elif eventname=="ok":  # OKボタンが押された時
					if dialog.getControl("PrecomposedPUAOption").getModel().State == True:
						umode = "PrecomposedPUA"
					elif dialog.getControl("CombiningOption").getModel().State == True:
						umode = "CombiningOnly"
					else:
						umode = "Precomposed"
					self.writeConfig(self.cfgnames, (str("300"), str("300"), str(umode)))  # 取得した値を文字列にしてコンポーネントデータノードに保存。
					
				elif eventname=="back":  # 元に戻すボタンが押された時
					maxwidth, maxheight, umode = self.readConfig(*self.cfgnames)
					umode = umode or self.defaults[2]
					maxwidth = maxwidth or self.defaults[0]
					maxheight = maxheight or self.defaults[1]
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
