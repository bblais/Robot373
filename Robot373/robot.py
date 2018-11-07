import time     # import the time library for the sleep function

def Wait(seconds):
    time.sleep(seconds)


try:
    import brickpi3 # import the BrickPi3 drivers
    BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
except ImportError:
    print("no module brickpi3")
    BP=None
    
def closest_color_as_number(r,g,b,*args):

    min_distance_sq=0
    min_color=None
    for c,color in enumerate(args):
        r2,g2,b2=color
        distance_sq=(r-r2)**2+(g-g2)**2+(b-b2)**2

        if min_color is None:  # first color
            min_color=c
            min_distance_sq=distance_sq
        elif distance_sq<min_distance_sq:
            min_color=c
            min_distance_sq=distance_sq
        else:
            pass

    return min_color


def closest_color(r,g,b,**kwargs):
    """
    C=closest_color(100,0,0,
            red=[100,0,0],
            glreen=[0,100,0],
            black=[100,100,100],
            )
    """
    min_distance_sq=0
    min_color=None

    for color in kwargs:

        r2,g2,b2=kwargs[color]

        distance_sq=(r-r2)**2+(g-g2)**2+(b-b2)**2

        if min_color is None:  # first color
            min_color=color
            min_distance_sq=distance_sq
        elif distance_sq<min_distance_sq:
            min_color=color
            min_distance_sq=distance_sq
        else:
            pass

    return min_color

class Timer(object):
    def __init__(self):
        self._reset()

    def _reset(self):
        self.t0=time.time()

    @property
    def time(self):
        return time.time()-self.t0

    @property
    def value(self):
        return time.time()-self.t0

    def seconds(self):
        return time.time()-self.t0    

class Sensor(object):

    def __init__(self,port,sensor_type):
        BP.set_sensor_type(port,sensor_type)
        self.port=port
        self.type=sensor_type
        self.BP=BP

    @property
    def value(self):
        try:
            val = BP.get_sensor(self.port)
        except brickpi3.SensorError as error:
            print(error)
            val=None

        return val

def Sensors2(one=None,two=None,three=None,four=None):

    sensors=[]
    for i,v in enumerate([one,two,three,four]):
        if not v:
            continue

        v=v.lower()

        ports=[BP.PORT_1,BP.PORT_2,BP.PORT_3,BP.PORT_4]

        if v=='ir' or v.startswith('infra'):
            sensors.append(Sensor(ports[i], BP.SENSOR_TYPE.EV3_INFRARED_PROXIMITY))
        elif v=='touch':
            sensors.append(Sensor(ports[i], BP.SENSOR_TYPE.TOUCH))
        elif v=='nxtus' or v.startswith('nxtultra'):
            sensors.append(Sensor(ports[i],  BP.SENSOR_TYPE.NXT_ULTRASONIC))
        elif v=='us' or v.startswith('ultra'):
            sensors.append(Sensor(ports[i],   BP.SENSOR_TYPE.EV3_ULTRASONIC_CM))
        elif v=='color':
            sensors.append(Sensor(ports[i], BP.SENSOR_TYPE.EV3_COLOR_COLOR_COMPONENTS))
        elif 'gyro' in v:
            sensors.append(Sensor(ports[i], BP.SENSOR_TYPE.EV3_GYRO_ABS_DPS))
        else:
            raise ValueError('Not implemented:' % v)

    if len(sensors)==0:
        return None
    elif len(sensors)==1:
        return sensors[0]
    else:
        return sensors
    

def Sensors(one=None,two=None,three=None,four=None):

    sensors=[]
    for i,v in enumerate([one,two,three,four]):
        if not v:
            sensors.append(None)
            continue

        v=v.lower()

        ports=[BP.PORT_1,BP.PORT_2,BP.PORT_3,BP.PORT_4]

        if v=='ir' or v.startswith('infra'):
            sensors.append(Sensor(ports[i], BP.SENSOR_TYPE.EV3_INFRARED_PROXIMITY))
        elif v=='touch':
            sensors.append(Sensor(ports[i], BP.SENSOR_TYPE.TOUCH))
        elif v=='nxtus' or v.startswith('nxtultra'):
            sensors.append(Sensor(ports[i],  BP.SENSOR_TYPE.NXT_ULTRASONIC))
        elif v=='us' or v.startswith('ultra'):
            sensors.append(Sensor(ports[i],   BP.SENSOR_TYPE.EV3_ULTRASONIC_CM))
        elif v=='color':
            sensors.append(Sensor(ports[i], BP.SENSOR_TYPE.EV3_COLOR_COLOR_COMPONENTS))
        elif 'gyro' in v:
            sensors.append(Sensor(ports[i], BP.SENSOR_TYPE.EV3_GYRO_ABS_DPS))
        else:
            raise ValueError('Not implemented:' % v)

    return sensors


class Motor(object):

    def __init__(self,port):
        self.port=port
        self._power=0
        self.reset_position()

    def reset_position(self):
        BP.offset_motor_encoder(self.port, BP.get_motor_encoder(self.port))

    @property
    def position(self):
        return BP.get_motor_encoder(self.port)

    @position.setter
    def position(self,pos):
        BP.set_motor_position(self.port, pos)

    @property
    def power(self):
        return self._power

    @power.setter
    def power(self,power):
        self._power=power
        BP.set_motor_power(self.port, power)        


def Motors(port_letters,size=None):
    m=[]
    unused=''
    ports=[BP.PORT_A,BP.PORT_B,BP.PORT_C,BP.PORT_D]
    for letter in port_letters:
        i=ord(letter.upper())-65
        m.append(Motor(ports[i]))
        
    if len(m)==0:
        return None
    elif len(m)==1:
        return m[0]
    else:
        return m

def Shutdown():
    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.



import os
from PIL import Image

def take_picture(filename='picture.jpg',view=False):

    a=os.system("fswebcam -S 20 --no-banner '%s'" % filename)
    print(a)
    if view:
        os.system('gpicview "%s" &' % filename)

def old_take_picture(filename='picture.jpg'):
    os.system("fswebcam -r 352x288 --no-banner '%s'" % filename)
