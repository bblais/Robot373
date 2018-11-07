from Robot373 import *

take_picture("my cool pic.jpg")

print('Pausing for a few seconds for another image, but with viewing')
for i in range(5,0,-1):
    print(i)
    Wait(1)
    
take_picture("my cool pic2.jpg",view=True)
