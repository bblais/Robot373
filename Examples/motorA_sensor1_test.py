from Robot373 import *

touch,S2,S3,S4=Sensors("touch",None,None,None)

Wait(3) # just to make sure we connect ok

Ma=Motors("a")

pressed=False

try:
    while True:
        if touch.value and not pressed:
            print("Button Pressed")
            pressed=True
            Ma.power=50
        elif not touch.value and pressed:
            print("Button Released")
            pressed=False
            Ma.power=0

    time.sleep(0.02)            
except KeyboardInterrupt:
    Ma.power=0


Shutdown()
