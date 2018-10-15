from Robot373 import *

S1,S2,S3,S4=Sensors(None,None,"us",None)

try:
    while True:
        distance=S1.value
        print(distance)
        Wait(0.05)
except KeyboardInterrupt:
    pass

Shutdown()
