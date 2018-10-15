from Robot373 import *

color_sensor=Sensors2(None,None,"color",None)

try:
    while True:
        value=color_sensor.value
        if not value:
            continue

        r,g,b,something=color_sensor.value
        print(r,g,b,something)
        print(closest_color(r,g,b,
                maroon=[128,0,0],
                gray=[128,128,128],
                white=[256,256,256],
                black=[0,0,0],
                ))
        Wait(0.05)
except KeyboardInterrupt:
    pass

Shutdown()
