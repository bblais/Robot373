from Robot373 import *
import os

if not os.path.exists('images'):
    print('Making folder "images"')
    os.mkdir('images')

count=0
while True:
    x=input('Hit enter to take a picture with no view.  Type any character and hit enter to take a picture with a view.')

    if x:
        view=True
    else:
        view=False

    fname='images/test%d.jpg' % count
    while os.path.exists(fname):
        count+=1
        fname='images/test%d.jpg' % count

    take_picture('images/test%d.jpg' % count,view=view)
    

