from Robot373 import *

Wait(3) # just to make sure we connect ok

touch,S2,S3,S4=Sensors("touch",None,None,None)

pressed=False

while True:
    if touch.value and not pressed:
        print("Button Pressed")
        pressed=True
    elif not touch.value and pressed:
        print("Button Released")
        pressed=False

