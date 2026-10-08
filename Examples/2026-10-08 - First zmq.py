#!/usr/bin/env python
# coding: utf-8

# In[1]:


from Robot373.zmq import *
client=setup_client(server_address='localhost:5555')


# # Set up Sensors and Motors

# In[2]:


left, right = Motors("ab")
touch,color,US = Sensors("touch", "color", "us", None)


# # Test Motors

# In[3]:


left.power = 30
right.power = 30
Wait(2)
left.power = 30
right.power = -30
Wait(2)
left.power = 0
right.power = -0


# # Test sensor values

# In[4]:


for i in range(3):
    value = color.value
    if value:
        print(f"  Reading {i+1}: R={value[0]}, G={value[1]}, B={value[2]}")
    else:
        print(f"  Reading {i+1}: None")
    Wait(0.2)


# In[5]:


for i in range(5):
    value = touch.value
    print(f"  Reading {i+1}: {value}")
    Wait(0.2)


# ## Test taking picture

# In[6]:


take_picture("my_cool_picture.jpg")


# # Shutdown

# In[7]:


Shutdown()


# In[ ]:




