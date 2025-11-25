
import journal

from pprint import pp

from time import time, sleep

lasttime=time()

while True:
    event=journal.read()

    if not event:
        sleep(0.5)
        continue
    print("%s [%s]" % (event['timestamp'], event['event']), end=" ")

    eventcopy=event.copy()
    del eventcopy['event']
    del eventcopy['timestamp']
    pp(eventcopy)
    
    timenow=time()
    sleep(1 if (1 > timenow-lasttime > 0.1) else 0)
    lasttime=timenow

    if("Shutdown" in event['event']):
        break

    print()
