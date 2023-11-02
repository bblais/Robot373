#!/usr/bin/env python
# coding: utf-8

# In[1]:


from Robot373 import *

touch=Sensors("touch",None,None,None)
Wait(3) # just to make sure we connect ok
Ma=Motors("a")
Ma.power=50

T=Timer()

while T.value<5:
    print(touch.value)
    Wait(.1)




Shutdown()


# In[ ]:




