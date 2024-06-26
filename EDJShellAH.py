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

print(ProgramName)
time.sleep(1.5)
print()

IgnoredEvents=['Music']
InterestingEvents=['Fileheader',
        'Cargo',
        'ReceiveText',
        'ReservoirReplenished',
        'Shutdown',
        ]

def handle_Shutdown(event):
    print("Game shut down")
    sys.exit(0)

########################################################################################################

JournalFile=open(CurJour, 'r')
Quit=False

N=0
Events=[]
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

    handlerName = "handle_"+eventType
    if handlerName in dir():
        print("Calling ", handlerName)
        exec("%s(event)" % (handlerName))
    else:
        print("Not found %s in %s" % ( handlerName, dir()))


# :      0.) <Fileheader> {'timestamp': '2024-06-24T04:29:02Z', 'event': 'Fileheader', 'part': 1, 'language': 'English/UK', 'Odyssey': True, 'gameversion': '4.0.0.1806', 'build': 'r302447/r0 '}






