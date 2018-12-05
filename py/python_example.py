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

        try:
            text = doc.Text
            cursor = text.createTextCursor()

            xIndexAccess = doc.getCurrentSelection()

            count = xIndexAccess.getCount();
            for i in range(count) :
                xTextRange = xIndexAccess.getByIndex(i);
                #print "string: " + xTextRange.getString();
                theString = xTextRange.getString();
                if len(theString)==0 :
                    # sadly we can have a selection where nothing is selected
                    # in this case we get the XWordCursor and make a selection!
                    xText = xTextRange.getText();
                    xWordCursor = xText.createTextCursorByRange(xTextRange);
                    if not xWordCursor.isStartOfWord():
                        xWordCursor.gotoStartOfWord(False);
                    xWordCursor.gotoNextWord(True);
                    theString = xWordCursor.getString();
                    newString = self.getBlah(); #theString.upper() #getNewString(theString);
                    if newString :
                        xWordCursor.setString(newString);
                        #cur.select(xWordCursor);
                    #text.insertString( cursor, "Hello World1", 0 )
                else :
                     newString = theString.upper() #getNewString( theString );
                     if newString:
                        xTextRange.setString( newString );
                        #cur.select(xTextRange);
                    #text.insertString( cursor, "Hello World2", 0 )
        except Exception as e:
            text.insertString( cursor, str(e), 6 )
            print('hello python to console')
            pass

        
g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(
        Example,
        "simple.example.identifier",
        ("com.sun.star.task.Job",),)             