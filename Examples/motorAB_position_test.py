from Robot373 import *

left,right=Motors("ab")

left.power=50
right.power=50

timer=Timer()
while timer.value<5:
    print(left.position,right.position)
    Wait(.1)

left.power=-50
right.power=-50

Wait(5)

Shutdown()
