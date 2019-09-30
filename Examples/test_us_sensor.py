from Robot373 import *

US=Sensors(None,None,"us",None)

try:
    while True:
        distance=US.value
        print(distance)
        Wait(0.05)
except KeyboardInterrupt:
    pass

Shutdown()
