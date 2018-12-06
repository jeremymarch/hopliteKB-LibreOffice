# -*- coding: utf-8 -*-
# make extension from repo directory: zip -r ../python_example.oxt * 

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

import uno
import unohelper

from com.sun.star.task import XJobExecutor

# gamma is a comb char, delta is a vowel
#gamma = b'\\u03b3' #just for testing
combiningAccents = [ b'\\u0304', b'\\u0306', b'\\u0308', b'\\u0314', b'\\u0313', b'\\u0301', b'\\u0300', b'\\u0342', b'\\u0342' ];
 
def accentLetter(letter):
        if letter == "ά":
            return "α"
        elif letter == "α":
            return "ά"
        else:
            return None

class Example( unohelper.Base, XJobExecutor ):
    def __init__( self, ctx ):
        self.ctx = ctx    

    def trigger( self, args ):
        
        try:
            desktop = self.ctx.ServiceManager.createInstanceWithContext( "com.sun.star.frame.Desktop", self.ctx )
 
            doc = desktop.getCurrentComponent()
            text = doc.Text;
            cursor = text.createTextCursor();

            xIndexAccess = doc.getCurrentSelection();
            xTextRange = xIndexAccess.getByIndex(0); #just the first selection
            xText = xTextRange.getText();
            xWordCursor = xText.createTextCursorByRange(xTextRange);
            xWordCursor.collapseToEnd();

            #go right to be sure the cursor we don't miss any combining chars, in case cursor is between them and letter; max 6
            n = 0
            for i in range(0, 6):
                xWordCursor.goRight(1, True);
                s = xWordCursor.getString();
                if s is not None and len(s) > 0 and s[-1].encode("unicode_escape") not in combiningAccents:
                    xWordCursor.collapseToStart(); #roll back one
                    break;
                n = n + 1;
                xWordCursor.collapseToEnd(); #go one by one

            #leave right fixed and go left until no more combining chars
            for j in range(0, 6 + n):
                xWordCursor.goLeft(1, True);
                s = xWordCursor.getString();
                if s is not None and len(s) > 0 and s[0].encode("unicode_escape") not in combiningAccents: #when != "a" this puts us one further past the comb. chars.
                    break;

            #get letter with any following combining chars, we decide what to do inside accentLetter
            letterToAccent = xWordCursor.getString();
            if letterToAccent is not None and len(letterToAccent) > 0:
                newLetter = accentLetter(letterToAccent)
                if newLetter is not None:
                    xWordCursor.setString(newLetter);

        except Exception as e:
            text.insertString( cursor, str(e), 0 ) #print exception
            #print('hello python to console')
            pass

        
g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(
        Example,
        "simple.example.identifier",
        ("com.sun.star.task.Job",),)
