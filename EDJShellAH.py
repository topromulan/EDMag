#!/bin/env python3

import os, time, glob, json

ProgramName="ED Journalist"
FakeInput=False
#FakeInput="/tmp/FAKER" #

if isinstance(FakeInput, str):
    ProgramName="ED Fake News Client: " + FakeInput
    CurJour="/tmp/FAKER.log"
else:
    CurJour=max(glob.glob("/shared/Journal*"), key=os.path.getctime)

print(ProgramName)

import time
time.sleep(1.5)

global JournalFile
JournalFile=open(CurJour, 'r')
Quit=False

N=0
Events=[]
IgnoredEvents=['Music']

def Absorb(event):
    eventType=event['event']
    if not eventType in IgnoredEvents:
        print(Events.index(event), eventType, event)

while not Quit:
    jsonLine=JournalFile.readline() #why it don't block
    time.sleep(0.005)
    if not jsonLine:
        memory=JournalFile.tell()
        time.sleep(2)
        JournalFile=open(CurJour, 'r')
        JournalFile.seek(memory)
        continue

    try:
        event=json.loads(jsonLine)
    except:
        print("\n\n\nERROR parsing", jsonLine);
        time.sleep(2)
        raise Exception("oh shit")

    #print(event['event'])
    Events.append(event)
    Absorb(event)









