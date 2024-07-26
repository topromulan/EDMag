#!/bin/env python3

import sys, os, time, glob, json
from pprint import pp

ProgramName="ED Journalist"
FakeInput=False
#FakeInput="/tmp/FAKER" #

if FakeInput:
    ProgramName="ED Fake News Client: " + FakeInput
    CurJour=FakeInput
else:
    CurJour=max(glob.glob("/shared/Journal*"), key=os.path.getctime)

IgnoredEvents=['Music', 'Friends', 'ShipLocker']
InterestingEvents=['Fileheader',
        'Cargo',
        'LoadGame',
        'Location',
        'MaterialCollected',
        'NpcCrewPaidWage',
        'ReceiveText',
        'ReservoirReplenished',
        'Scan',
        'Shutdown',
        'Statistics',
        ]

InitialRead=True
WasInteresting=False

########################################################################################################

def vt100(*codes):
    for code in codes:
        print("\x1b[%s" % code)


def hanging_exam(event, thoughts="look at it. do something with it."):
    #vt100("2J", "H", "0;1M")
    print( ("#"*18 + " %s " % event['event'].upper())*3, "EVENT: ", event['event'])
    vt100("0M")
    pp(event, width=4)
    if not InitialRead:
        time.sleep(0.5); print("%s -- TODO: %s" % ('#'*45, thoughts))
        time.sleep(3.5)
    time.sleep(0.5); print("#"*60,"\n")


########################################################################################################

global ED_fn_prefix
ED_fn_prefix="handle_ED_"

def handle_ED_Shutdown(event):
    print("Game shut down")
    sys.exit(0)

def handle_ED_Location(event):
    hanging_exam(event, "put this in a .dat file to watch in a pinned window")

def handle_ED_Liftoff(event):
    hanging_exam(event)

SAASignalsFound={}
def handle_ED_SAASignalsFound(event):
    global SAASignalsFound
    SAASignalsFound[event['BodyName']] = [g['Genus_Localised'] for g in event['Genuses']]

def handle_ED_Touchdown(event):
    bodyName=event['Body']
    if bodyName in SAASignalsFound:
        vt100("0;1;35M")
        print("SAA Signals Found: ", SAASignalsFound[bodyName])
        vt100("0M")

########################################################################################################

JournalFile=open(CurJour, 'r')
Quit=False

N=0
Events=[]
Handlers=[fnName for fnName in dir() if fnName.startswith(ED_fn_prefix)]

print(ProgramName)
print(Handlers)
print("Opening", CurJour)
time.sleep(1.5)
print()
time.sleep(.5)

while not Quit:
    jsonLine=JournalFile.readline()
    time.sleep(0.05 if FakeInput else 0.00125)
    if not jsonLine:
        memory=JournalFile.tell()
        time.sleep(2)
        JournalFile=open(CurJour, 'r')
        JournalFile.seek(memory)
        InitialRead=False
        continue

    try:
        event=json.loads(jsonLine)
    except:
        print("\n\n\nERROR parsing", jsonLine);
        time.sleep(2)
        raise Exception("oh shit")

    Events.append(event)
    eventType=event['event']
    if eventType in InterestingEvents and not WasInteresting:
        if len(str(event)) > 80:
            print("")
        print('<'+eventType+'>', str(event)[:120])
        WasInteresting=True
        # Log it to a file and shorten this preview
    elif not eventType in IgnoredEvents:
        print("|%7d.) " % Events.index(event), end='')
        print(".. %8d bytes (%s) \t.. %50s .." % (len(str(event)), eventType, str(event)[:50]))
    else:
        WasInteresting=False

    handlerName = ED_fn_prefix+eventType
    if handlerName in dir():
    #if handlerName.isidentifier(): hmmm
        print("Calling ", handlerName)
        exec("%s(event)" % (handlerName))
    else:
        pass


# :      0.) <Fileheader> {'timestamp': '2024-06-24T04:29:02Z', 'event': 'Fileheader', 'part': 1, 'language': 'English/UK', 'Odyssey': True, 'gameversion': '4.0.0.1806', 'build': 'r302447/r0 '}






