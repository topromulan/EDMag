#!/bin/env python3

import sys, os, time, glob, json

ProgramName="ED Journalist"
FakeInput=False
#FakeInput="/tmp/FAKER" #

if isinstance(FakeInput, str):
    ProgramName="ED Fake News Client: " + FakeInput
    CurJour="/tmp/FAKER.log"
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
time.sleep(1.5)
print()

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
        print('<'+eventType+'>', event)
        if len(str(event)) > 80:
            print()
    elif not eventType in IgnoredEvents:
        print("|%7d.) " % Events.index(event), end='')
        print(".. %8d bytes (%s)" % (len(str(event)), eventType))
    else:
        pass

    handlerName = ED_fn_prefix+eventType
    if handlerName in dir():
        print("Calling ", handlerName)
        exec("%s(event)" % (handlerName))
    else:
        pass


# :      0.) <Fileheader> {'timestamp': '2024-06-24T04:29:02Z', 'event': 'Fileheader', 'part': 1, 'language': 'English/UK', 'Odyssey': True, 'gameversion': '4.0.0.1806', 'build': 'r302447/r0 '}






