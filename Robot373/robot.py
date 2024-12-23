from cmath import tau
import time     # import the time library for the sleep function

def Wait(seconds):
    time.sleep(seconds)


try:
    import brickpi3 # import the BrickPi3 drivers
    BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
except ImportError:
    print("no module brickpi3...running in offline mode")
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
        if not BP is None:
            BP.set_sensor_type(port,sensor_type)
        self.port=port
        self.type=sensor_type
        self.BP=BP
        self.called_once=False
        self.T=Timer()
        self.T._reset()

    @property
    def value(self):
        def sine_value(T,tau,value_min,value_max):
            return (value_max-value_min)*(sin(T.value/tau*2*3.14159)+1)/2+value_min

        from math import sin  # used for fake data
        if not BP is None:
            try:
                val = BP.get_sensor(self.port)
            except brickpi3.SensorError as error:
                print(error)
                val=None
        else:  # do a random value for the sensor
            if not self.called_once:
                print(f"Warning -- Sensor {self.type} in offline mode.  Returning fake data.")
                self.called_once=True

            if self.type in ['ir','nxtus','us','gyro']:
                tau=10  # seconds
                value_min=0
                value_max=50

                return int(sine_value(self.T,10,0,50))
            elif self.type in ['touch']:
                tau=10  # seconds
                value_min=0
                value_max=50
                return sine_value(self.T,10,0,50)>25
            elif self.type in ['color']:
                tau=10  # seconds
                value_min=0
                value_max=255
                return [int(sine_value(self.T,10,0,255)),
                        int(sine_value(self.T,15,0,255)),
                        int(sine_value(self.T,7.6,0,255)),                        
                        100]
            else:
                return None

            val=None

        return val

def Sensors(S1=None,S2=None,S3=None,S4=None):

    sensors=[]
    for i,v in enumerate([S1,S2,S3,S4]):
        if not v:
            continue

        v=v.lower()

        if not BP is None:
            ports=[BP.PORT_1,BP.PORT_2,BP.PORT_3,BP.PORT_4]
        else:
            ports=[1,2,3,4]

        if not BP is None:
            D={
                'ir':BP.SENSOR_TYPE.EV3_INFRARED_PROXIMITY,
                'infra':BP.SENSOR_TYPE.EV3_INFRARED_PROXIMITY,
                'nxtus':BP.SENSOR_TYPE.NXT_ULTRASONIC,
                'nxtultra':BP.SENSOR_TYPE.NXT_ULTRASONIC,
                'us':BP.SENSOR_TYPE.EV3_ULTRASONIC_CM,
                'touch':BP.SENSOR_TYPE.TOUCH,
                'ultra':BP.SENSOR_TYPE.EV3_ULTRASONIC_CM,
                'color':BP.SENSOR_TYPE.EV3_COLOR_COLOR_COMPONENTS,
                'gyro':BP.SENSOR_TYPE.EV3_GYRO_ABS_DPS,
            }
        else:

            D={
                'ir':'ir',
                'infra':'ir',
                'nxtus':'nxtus',
                'nxtultra':'nxtus',
                'us':'us',
                'ultra':'us',
                'touch':'touch',
                'color':'color',
                'gyro':'gyro',
            }

        found=False
        for key in D:
            if v.startswith(key):
                sensors.append(Sensor(ports[i], D[key]))
                found=True
                break

        if not found:
            raise ValueError('Not implemented: "%s"' % str(v))

    if sensors:
        warm_up_sensors(sensors)

    if len(sensors)==0:
        return None
    elif len(sensors)==1:
        return sensors[0]
    else:
        return sensors

from io import StringIO 
import sys

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout


def warm_up_sensors(*args):
    import contextlib

    print("Waiting for Sensors to Warm Up...",end="")
    sys.stdout.flush()

    if isinstance(args[0],list):
        sensors=args[0]
    else:
        sensors=args

    if BP is None:
        print("Offline mode for sensors...done.")
        return


    T=Timer()
    with Capturing() as output:
        while True:
            still_warming_up=False
            for sensor in sensors:
                if sensor.value is None:
                    still_warming_up=True
                    continue
            if not still_warming_up:
                break

            Wait(0.05)

            if T.value>10:
                break

    if T.value>10:
        print("Waited for 10 seconds...still not reading sensors...")

    print("done.")

    
def Sensors2(*args,**kwargs):
    raise ValueError("Use Sensors() instead of Sensors2()")

def Sensors_old(one=None,two=None,three=None,four=None):

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
            raise ValueError('Not implemented: "%s"' % str(v))

    return sensors


# set_motor_power will set the PWM duty cycle percentage. At 10v battery voltage and a PWM duty cycle (power level) of 25%, the motor would get an average of 2.5v (not factoring voltage drop at a few points). You can set the power level to anything from -100 to 100 (full reverse to full forward) with 1% precision. You can set the power level to -128 to float the motor (make it rotate freely as if the cable was disconnected). In this mode, the power applied to the motor is not regulated by speed or position, so it wont compensate for varying load etc.

# set_motor_dps will set a target speed for the motor to run (in Degrees Per Second). The robots firmware (BP3 or GPG3) will use the encoder feedback to determine the current position/speed of the motor, and adjust the PWM power in attempt to maintain the target speed.

# The most recent command overrides previous commands. For example, if you set the target speed to 100dps with set_motor_dps and then 2 seconds later tell the motor to float to a stop by setting -128 with set_motor_power, the motor will run at 100dps and then float (do the most recent command).

# With set_motor_limits, the power limit is the maximum PWM value that the firmware will apply while attempting to run at the specified speed target or position target. The dps limit is the maximum speed that the firmware will allow the motor to run while attempting to reach a position target.





class Motor(object):

    def __init__(self,port):
        self.port=port
        self._power=0
        self._position=0
        self._dps=None
        self.T=Timer()
        self.T._reset()
        self.last_position=0 # for fake data
        self.called_once=False

        self.reset_position()

    def reset_position(self):
        if not BP is None:
            BP.offset_motor_encoder(self.port, BP.get_motor_encoder(self.port))
        else:
            self._position=0
            self.last_position=0
            self.T._reset()

        self._position=self.position

    @property
    def degrees_per_second(self):
        return self._dps


    @degrees_per_second.setter
    def degrees_per_second(self,dps):
        if not BP is None:
            BP.set_motor_dps(self.port, dps = dps)
        self._dps=dps


    @property
    def position(self):
        if not BP is None:
            self._position=BP.get_motor_encoder(self.port)
        else:
            if not self.called_once:
                print(f"Warning -- Motor {self.port} in offline mode.  Returning fake data.")
                self.called_once=True

            self._position=int(self.power/3*self.T.value+self.last_position)


        return self._position

    @position.setter
    def position(self,pos):
        if not BP is None:
            BP.set_motor_position(self.port, pos)
        else:
            self.last_position=pos
            self.T._reset()

        self._position=pos            

    @property
    def power(self):
        return self._power

    @power.setter
    def power(self,power):
        if not BP is None:
            BP.set_motor_power(self.port, power)
        else:
            self.last_position=int(self.power/3*self.T.value+self.last_position)
            self.T._reset()
        self._power=power


    def drive(self,power,distance,verbose=False):
        start=self.position
        self.power=power
        end=self.position
        while abs(end-start)<distance:
            if verbose:
                print("position: ",self.position, "end",end)
            end=self.position
            Wait(0.01)

        self.power=0
        

def Motors(port_letters,size=None):
    m=[]
    unused=''

    if not BP is None:
        ports=[BP.PORT_A,BP.PORT_B,BP.PORT_C,BP.PORT_D]
    else:
        ports=[1,2,3,4]


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
    if not BP is None:
        BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
    print("Shutdown.")



import os
from PIL import Image

def take_picture(filename='picture.jpg',brightness=100,view=False,S=10):
    cmd=f"fswebcam -s brightness={brightness}%% -r 1600x900 --no-banner -S {S} '{filename}'"
    print(cmd)
    a=os.system(cmd)
    print(a)

def old_take_picture(filename='picture.jpg'):
    os.system("fswebcam -r 352x288 --no-banner '%s'" % filename)
