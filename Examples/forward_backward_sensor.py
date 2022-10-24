from Robot373 import *

touch=Sensors("touch",None,None,None)
Wait(3) # just to make sure we connect ok
Ma=Motors("a")


Ma.power=50
Wait(3)




Shutdown()
