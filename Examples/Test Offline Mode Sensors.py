#!/usr/bin/env python
# coding: utf-8

# In[1]:


from Robot373 import *

touch,color,eyes=Sensors("touch","color","us",None)
Wait(3) # just to make sure we connect ok
Ma=Motors("a")
Ma.power=50

T=Timer()

while T.value<10:
    print(eyes.value)
    Wait(.2)




Shutdown()


# In[2]:


from Robot373 import *

touch,color,eyes=Sensors("touch","color","us",None)
Wait(3) # just to make sure we connect ok
Ma=Motors("a")
Ma.power=50

T=Timer()

while T.value<5:
    print(color.value)
    Wait(.2)




Shutdown()


# In[3]:


from Robot373 import *

touch,color,eyes=Sensors("touch","color","us",None)
Wait(3) # just to make sure we connect ok
Ma=Motors("a")
print("forward")
Ma.power=50

T=Timer()
while T.value<5:
    print(Ma.position)
    Wait(.2)

print("reverse")
Ma.power=-100

T=Timer()
while T.value<5:
    print(Ma.position)
    Wait(.2)



Shutdown()


# In[ ]:




