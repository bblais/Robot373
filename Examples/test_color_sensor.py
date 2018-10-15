from Robot373 import *

color_sensor=Sensors2(None,None,"color",None)

try:
    while True:
        color=color_sensor.value
        print(color)
        Wait(0.05)
except KeyboardInterrupt:
    pass

Shutdown()
