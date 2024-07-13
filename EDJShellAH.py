#!/bin/env python3

import sys, os, time, glob, json

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
        'Shutdown',
        'Statistics',
        ]

########################################################################################################

global ED_fn_prefix
ED_fn_prefix="handle_ED_"

def handle_ED_Shutdown(event):
    print("Game shut down")
    sys.exit(0)

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
    time.sleep(0.00025)
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

    Events.append(event)
    eventType=event['event']
    if eventType in InterestingEvents:
        if len(str(event)) > 80:
            print("")
        print('<'+eventType+'>', str(event)[:120])
        # Log it to a file and shorten this preview

    elif not eventType in IgnoredEvents:
        print("|%7d.) " % Events.index(event), end='')
        print(".. %8d bytes (%s) \t.. %50s .." % (len(str(event)), eventType, str(event)[:50]))
    else:
        pass

    handlerName = ED_fn_prefix+eventType
    if handlerName in dir():
    #if handlerName.isidentifier(): hmmm
        print("Calling ", handlerName)
        exec("%s(event)" % (handlerName))
    else:
        pass


# :      0.) <Fileheader> {'timestamp': '2024-06-24T04:29:02Z', 'event': 'Fileheader', 'part': 1, 'language': 'English/UK', 'Odyssey': True, 'gameversion': '4.0.0.1806', 'build': 'r302447/r0 '}






