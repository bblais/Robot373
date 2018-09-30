import time     # import the time library for the sleep function

try:
    import brickpi3 # import the BrickPi3 drivers
    BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
except ImportError:
    print("no module brickpi3")
    BP=None
    
def closest_color(r,g,b,**kwargs):
    """
    C=closest_color(100,0,0,
            red=[100,0,0],
            green=[0,100,0],
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

    def time(self):
        return time.time()-self.t0

    def seconds(self):
        return time.time()-self.t0    

class Sensor(object):

    def __init__(self,port,sensor_type):
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

    

def Sensors(one=None,two=None,three=None,four=None):

    sensors=[]
    for i,v in enumerate([one,two,three,four]):
        if not v:
            sensors.append(None)
            continue

        v=v.lower()

        ports=[BP.PORT_1,BP.PORT_2,BP.PORT_3,BP.PORT_4]

        if v=='ir' or v.startswith('infra'):
            sensors.append(Sensor(BP.set_sensor_type(ports[i], BP.SENSOR_TYPE.EV3_INFRARED_PROXIMITY)))
        elif v=='touch':
            sensors.append(Sensor(BP.set_sensor_type(ports[i], BP.SENSOR_TYPE.TOUCH)))
        elif v=='us' or v.startswith('ultra'):
            sensors.append(Sensor(BP.set_sensor_type(ports[i],  BP.SENSOR_TYPE.NXT_ULTRASONIC)))
        elif v=='color':
            sensors.append(Sensor(BP.set_sensor_type(ports[i], BP.SENSOR_TYPE.EV3_COLOR_COLOR_COMPONENTS)))
        elif 'gyro' in v:
            sensors.append(Sensor(BP.set_sensor_type(ports[i], BP.SENSOR_TYPE.EV3_GYRO_ABS_DPS)))
        else:
            raise ValueError('Not implemented:' % v)

    return sensors


class Motor(object):

    def __init__(self,port):
        self.port=port
        self._power=0

    @property
    def power(self):
        return BP.get_motor_encoder(self.port)

    @power.setter
    def power(self,power):
        self._power=_power
        BP.set_motor_power(port, power)        


def Motors(port_letters,size=None):
    m=[]
    unused=''
    ports=[BP.PORT_A,BP.PORT_B,BP.PORT_C,BP.PORT_D]
    for letter in port_letters:
        i=ord(letter.upper())-65
        m.append(Motor(ports[i]))

    return m
