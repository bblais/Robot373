from Robot373 import *

color_sensor=Sensors(None,None,"color",None)
left,right=Motors("ab")

left.power=50
right.power=50

values=[]
try:
    while True:
        value=color_sensor.value
        if not value:
            continue

        r,g,b,something=color_sensor.value
        print(r,g,b,something)

        maroon=[128,0,0]
        gray=[128,128,128]
        white=[256,256,256]
        black=[0,0,0]

        col=closest_color_as_number(r,g,b,
                maroon,gray,white,black
                )
        values.append(col)
        print(col)

        if col==3:  # black
            break

        Wait(0.05)
except KeyboardInterrupt:
    pass


Shutdown()

print(values)

