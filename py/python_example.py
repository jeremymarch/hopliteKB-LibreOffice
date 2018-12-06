# -*- coding: utf-8 -*-
# from repo: zip -r ../python_example.oxt * 

import uno
import unohelper


from com.sun.star.task import XJobExecutor
 
class Example( unohelper.Base, XJobExecutor ):
    def __init__( self, ctx ):
        self.ctx = ctx

    def getNewString( theString ) :
        if not theString or len(theString) ==0 :
            return ""
        # should we tokenize on "."?
        if theString[0].isupper() and len(theString)>=2 and theString[1].isupper() :
        # first two chars are UC => first UC, rest LC
            newString=theString.capitalize();
        elif theString[0].isupper():
        # first char UC => all to LC
            newString=theString.lower()
        else: # all to UC.
            newString=theString.upper()
        return newString;

    def getBlah(self):
        return "BlAh"        

    def trigger( self, args ):
        desktop = self.ctx.ServiceManager.createInstanceWithContext(
            "com.sun.star.frame.Desktop", self.ctx )
 
        doc = desktop.getCurrentComponent()

#get char to right
#if combining, move right until not combining char
#select left until not combining
#if it's a vowel or rho, this is our string.

#these two are the main basis of this extension
#https://forum.openoffice.org/en/forum/viewtopic.php?t=70633
#https://wiki.openoffice.org/wiki/PyUNO_samples

#https://ask.libreoffice.org/en/question/12614/python-macro-to-insert-text-at-gui-cursor-position/
#https://stackoverflow.com/questions/49728663/enumerate-fieldmarks-in-a-libreoffice-document#49735882

#https://github.com/slgobinath/libreoffice-code-highlighter/blob/master/codehighlighter/python/highlight.py
#https://github.com/kelsa-pi/unodit

#com sun star text XTextCursor : https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1text_1_1XTextCursor.html
#keyboard stuff: https://github.com/XRoemer/Organon/blob/master/source/py/shortcuts.py

#chart: https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1frame_1_1XModel.html#a1ee3a9fe564e0757381e23ef1a401eef

#iterate by char (java) https://stackoverflow.com/questions/38124658/how-to-navigate-through-each-character-in-open-office

#useful c++ guide: https://wiki.openoffice.org/wiki/Writer/API/Overview#The_XTextCursor_Interface
#and this: https://wiki.openoffice.org/wiki/Uno/Cpp/Tutorials/Introduction_to_Cpp_Uno

#https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1text_1_1XTextCursor.html

#we'll need to go one by one and then save end loc in a range, then create new range if vowel is found
#this is because we can't shrink the range once we find the right end of the combining chars.
        try:
            text = doc.Text;
            cursor = text.createTextCursor();

            xIndexAccess = doc.getCurrentSelection();
            xTextRange = xIndexAccess.getByIndex(0);
            xText = xTextRange.getText();
            xWordCursor = xText.createTextCursorByRange(xTextRange);
            xWordCursor.collapseToEnd();

            # gamma is a comb char, delda is a vowel
            gamma = b'\\u03b3' #just for testing
            combiningAccents = [gamma, b'\\u0304', b'\\u0306', b'\\u0308', b'\\u0314', b'\\u0313', b'\\u0301', b'\\u0300', b'\\u0342', b'\\u0342' ];

            #go to right until no more combining chars
            n = 0
            for i in range(0, 6):
                xWordCursor.goRight(1, True);
                s = xWordCursor.getString();
                if s is not None and len(s) > 0 and s[-1].encode("unicode_escape") not in combiningAccents:
                    xWordCursor.collapseToStart(); #roll back one
                    break;
                n = n + 1
                xWordCursor.collapseToEnd(); #go one by one

            #theString = xWordCursor.getString();
            #xWordCursor.setString(theString.upper());

            #leave right fixed and go left until no more combining chars
            for j in range(0, 6 + n):
                xWordCursor.goLeft(1, True);
                s = xWordCursor.getString();
                if s is not None and len(s) > 0 and s[0].encode("unicode_escape") not in combiningAccents: #when != "a" this puts us one further past the comb. chars.
                    break;

            #if first char is a vowel, then we proceed
            s = xWordCursor.getString();
            if s is not None and len(s) > 0 and s[0] == "δ":
                theString = xWordCursor.getString();
                xWordCursor.setString(theString.upper());
            
            #text.insertString( cursor, theString, 6 )

            # #count = xIndexAccess.getCount();
            # #for i in range(count) :
            # xTextRange = xIndexAccess.getByIndex(0);
            # #print "string: " + xTextRange.getString();
            # theString = xTextRange.getString();
            # if len(theString)==0 :
            #     # sadly we can have a selection where nothing is selected
            #     # in this case we get the XWordCursor and make a selection!
            #     xText = xTextRange.getText();
            #     xWordCursor = xText.createTextCursorByRange(xTextRange);
            #     if not xWordCursor.isStartOfWord():
            #         xWordCursor.gotoStartOfWord(False);
            #     xWordCursor.gotoNextWord(True);
            #     theString = xWordCursor.getString();
            #     newString = self.getBlah(); #theString.upper() #getNewString(theString);
            #     if newString :
            #         xWordCursor.setString(newString);
            #         #cur.select(xWordCursor);
            #     #text.insertString( cursor, "Hello World1", 0 )
            # else :
            #      newString = theString.upper() #getNewString( theString );
            #      if newString:
            #         xTextRange.setString( newString );
            #         #cur.select(xTextRange);
            #     #text.insertString( cursor, "Hello World2", 0 )
        except Exception as e:
            text.insertString( cursor, str(e), 6 )
            print('hello python to console')
            pass

        
g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(
        Example,
        "simple.example.identifier",
        ("com.sun.star.task.Job",),)             