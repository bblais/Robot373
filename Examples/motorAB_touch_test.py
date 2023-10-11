from Robot373 import *
touch=Sensors("touch",None,None,None)
left,right=Motors("ab")
Wait(3) # just to make sure we connect ok
print("Starting...")
try:
    while True:
        if touch.value:
            left.power=0
            right.power=0
        else:
            left.power=50
            right.power=50
except KeyboardInterrupt:
    pass

print("Ending.")

Shutdown()
