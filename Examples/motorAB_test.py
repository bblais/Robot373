from Robot373 import *

left,right=Motors("ab")

pressed=False

left.power=50
right.power=50

Wait(5)

left.power=-50
right.power=-50

Wait(5)

Shutdown()
