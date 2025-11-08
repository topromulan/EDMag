#!/bin/env python3

import sys, os, time, glob, json

FakeInput=False
#FakeInput="/tmp/FAKER" #

JournalDirVBox="/shared"
JournalDirWSL="/mnt/c/Users/limed/Saved Games/Frontier Developments/Elite Dangerous"
JournalDirWin="c:\\Users\\limed\\Saved Games\\Frontier Developments\\Elite Dangerous"

#JournalDir=JournalDirVBox; JournalReopenKluge=True
JournalDir=JournalDirWSL; JournalReopenKluge=False
#JournalDir=JournalDirWin; JournalReopenKluge=False

JournalDir=JournalDir[:-1] if JournalDir[-1] in "\\/" else JournalDir

# XXX Check if this works for run in IDLE
# XXX and check standard library way to do it
#PathSeparator='\\'
#PathSeparator='/'
PathSeparator='/' if '/' in JournalDir else '\\'

JournalDir=JournalDir.replace('/', PathSeparator).replace('\\', PathSeparator)
print("Journal dir: ", JournalDir)

if FakeInput:
    CurJour=FakeInput
else:
    JournalGlobString="%s%sJournal*" % (JournalDir, PathSeparator)
    CurJour=max(glob.glob(JournalGlobString), key=os.path.getctime)
print("Current Journal: ", CurJour)
print()

JournalFile=open(CurJour, 'r')

def read():
    jsonLine=JournalFile.readline()
    try:
        event=json.loads(jsonLine)
    except Exception as e:
        if 'Expecting value' in e.msg:
            return None
        time.sleep(2)
        raise Exception("oh shit")

    return event
    

