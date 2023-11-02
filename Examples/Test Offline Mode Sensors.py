#!/usr/bin/env python
# coding: utf-8

# In[4]:


from Robot373 import *

touch,color,eyes=Sensors("touch","color","us",None)
Wait(3) # just to make sure we connect ok
Ma=Motors("a")
Ma.power=50

T=Timer()

while T.value<10:
    print(color.value)
    Wait(.2)




Shutdown()


# In[ ]:




