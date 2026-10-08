"""
Robot373 ZMQ Client Library
This module provides the same API as robot.py but communicates with a remote server via ZMQ.
"""

import time
import zmq
import json

# Configuration
VERBOSE = False  # Set to True to see all commands and responses


def set_verbose(verbose=True):
    """Enable or disable verbose output"""
    global VERBOSE
    VERBOSE = verbose
    print(f"Verbose mode: {'ON' if verbose else 'OFF'}")


def Wait(seconds):
    time.sleep(seconds)

class ZMQClient:
    """ZMQ client for communicating with the robot server"""
    
    def __init__(self, server_address='localhost:5555'):
        self.context = zmq.Context()
        self.socket = None
        self._connected = False  
        
        # Parse server address
        if ':' in server_address:
            host, port = server_address.split(':')
            self.server_address = f"tcp://{host}:{port}"
        else:
            self.server_address = f"tcp://{server_address}:5555"

        self._connect()

    # Test the connection with a ping command
        self._test_connection()
    
    def _test_connection(self):
        """Test the connection by sending a ping command"""
        try:
            # Send a simple command to verify connection
            response = self.send_command({"method": "ping"})
            # Connection successful (send_command will print "done")
        except ConnectionError:
            # Re-raise to stop execution
            raise
    

    def _connect(self):
        """Connect or reconnect to the server"""
        if self.socket:
            self.socket.close()
    
        self.socket = self.context.socket(zmq.REQ)
        self.socket.setsockopt(zmq.RCVTIMEO, 5000)
        self.socket.setsockopt(zmq.SNDTIMEO, 5000)
        self.socket.setsockopt(zmq.LINGER, 0)
        self.socket.setsockopt(zmq.SNDHWM, 0)  # Don't queue send messages
        self.socket.setsockopt(zmq.RCVHWM, 0)  # Don't queue receive messages
    
        print(f"Connecting to robot server at {self.server_address}...", end="", flush=True)
        self.socket.connect(self.server_address)
    
    
    def send_command(self, command_dict):
        """Send a command and receive response with auto-reconnect"""
        max_retries = 3
        retry_count = 0
        
        if VERBOSE:
            print(f"[CLIENT → SERVER] {command_dict}")
        
        while retry_count < max_retries:
            try:
                # Send command
                self.socket.send_json(command_dict)
                
                # Receive response
                response = self.socket.recv_json()
                
                # Print "done" on first successful connection
                if not hasattr(self, '_connected'):
                    print("done")
                    self._connected = True
                
                if VERBOSE:
                    print(f"[SERVER → CLIENT] {response}")
                
                if response.get("status") == "error":
                    print(f"Server error: {response.get('message')}")
                    return None
                
                return response.get("value")
                
            except zmq.Again:
                retry_count += 1
                if retry_count == 1:
                    print("failed")
                print(f"Warning: Request timeout. Attempt {retry_count}/{max_retries}")
                if retry_count < max_retries:
                    self._connect()
                    
            except zmq.ZMQError as e:
                retry_count += 1
                if retry_count == 1:
                    print("failed")
                print(f"Warning: ZMQ Error: {e}")
                if retry_count < max_retries:
                    time.sleep(0.5)
                    self._connect()
        
        # If we get here, all retries failed
        print("Error: Failed to communicate with server after 3 attempts")
        print("Please check that the server is running.")
        raise ConnectionError("Unable to connect to robot server")
        
# Global client instance
_client = None

def get_client(server_address=None):
    global _client
    if _client is None:
        if server_address is None:
            server_address = f"{ROBOT_SERVER}:{ROBOT_PORT}"
        _client = ZMQClient(server_address)
    return _client


def setup_client(server_address='localhost:5555', verbose=False):
    """
    Setup the ZMQ client connection.
    Call this at the start of your script to configure the server.
    
    Args:
        server_address: Server address in format 'hostname:port' or just 'hostname'
        verbose: Enable verbose output
    
    Example:
        setup_client('192.168.1.100:5555', verbose=True)
        setup_client('localhost')  # Uses default port 5555
    """
    global _client, VERBOSE
    VERBOSE = verbose
    _client = ZMQClient(server_address)
    if verbose:
        print(f"Verbose mode: ON")
    return _client


    
def closest_color_as_number(r, g, b, *args):
    min_distance_sq = 0
    min_color = None
    for c, color in enumerate(args):
        r2, g2, b2 = color
        distance_sq = (r - r2)**2 + (g - g2)**2 + (b - b2)**2

        if min_color is None:  # first color
            min_color = c
            min_distance_sq = distance_sq
        elif distance_sq < min_distance_sq:
            min_color = c
            min_distance_sq = distance_sq

    return min_color


def closest_color(r, g, b, **kwargs):
    """
    C=closest_color(100,0,0,
            red=[100,0,0],
            green=[0,100,0],
            black=[100,100,100],
            )
    """
    min_distance_sq = 0
    min_color = None

    for color in kwargs:
        r2, g2, b2 = kwargs[color]
        distance_sq = (r - r2)**2 + (g - g2)**2 + (b - b2)**2

        if min_color is None:  # first color
            min_color = color
            min_distance_sq = distance_sq
        elif distance_sq < min_distance_sq:
            min_color = color
            min_distance_sq = distance_sq

    return min_color


class Timer(object):
    def __init__(self):
        self._reset()

    def _reset(self):
        self.t0 = time.time()

    @property
    def time(self):
        return time.time() - self.t0

    @property
    def value(self):
        return time.time() - self.t0

    def seconds(self):
        return time.time() - self.t0


class Sensor(object):
    def __init__(self, port, sensor_type):
        self.port = port
        self.type = sensor_type
        self.client = get_client()
        
        # Initialize sensor on server
        command = {
            "method": "init_sensor",
            "port": port,
            "sensor_type": sensor_type
        }
        self.client.send_command(command)

    @property
    def value(self):
        command = {
            "method": "get_sensor_value",
            "port": self.port
        }
        return self.client.send_command(command)


def Sensors(S1=None, S2=None, S3=None, S4=None):
    sensors = []
    
    # Port mapping
    ports = [1, 2, 3, 4]
    
    # Sensor type mapping
    sensor_types = {
        'ir': 'ir',
        'infra': 'ir',
        'nxtus': 'nxtus',
        'nxtultra': 'nxtus',
        'us': 'us',
        'ultra': 'us',
        'touch': 'touch',
        'color': 'color',
        'gyro': 'gyro',
    }
    
    for i, v in enumerate([S1, S2, S3, S4]):
        if not v:
            continue

        v = v.lower()
        
        found = False
        for key in sensor_types:
            if v.startswith(key):
                sensors.append(Sensor(ports[i], sensor_types[key]))
                found = True
                break

        if not found:
            raise ValueError('Not implemented: "%s"' % str(v))

    if sensors:
        warm_up_sensors(sensors)

    if len(sensors) == 0:
        return None
    elif len(sensors) == 1:
        return sensors[0]
    else:
        return sensors


def warm_up_sensors(*args):
    print("Waiting for Sensors to Warm Up...", end="")
    
    if isinstance(args[0], list):
        sensors = args[0]
    else:
        sensors = args

    T = Timer()
    while True:
        still_warming_up = False
        for sensor in sensors:
            if sensor.value is None:
                still_warming_up = True
                continue
        if not still_warming_up:
            break

        Wait(0.05)

        if T.value > 10:
            break

    if T.value > 10:
        print("Waited for 10 seconds...still not reading sensors...")

    print("done.")


class Motor(object):
    def __init__(self, port):
        self.port = port
        self.client = get_client()
        self._power = 0
        self._dps = None
        
        # Initialize motor on server
        command = {
            "method": "init_motor",
            "port": port
        }
        self.client.send_command(command)

    def reset_position(self):
        command = {
            "method": "reset_motor_position",
            "port": self.port
        }
        self.client.send_command(command)

    @property
    def degrees_per_second(self):
        return self._dps

    @degrees_per_second.setter
    def degrees_per_second(self, dps):
        command = {
            "method": "set_motor_dps",
            "port": self.port,
            "dps": dps
        }
        self.client.send_command(command)
        self._dps = dps

    @property
    def position(self):
        command = {
            "method": "get_motor_position",
            "port": self.port
        }
        return self.client.send_command(command)

    @position.setter
    def position(self, pos):
        command = {
            "method": "set_motor_position",
            "port": self.port,
            "position": pos
        }
        self.client.send_command(command)

    @property
    def power(self):
        return self._power

    @power.setter
    def power(self, power):
        command = {
            "method": "set_motor_power",
            "port": self.port,
            "power": power
        }
        self.client.send_command(command)
        self._power = power

    def drive(self, power, distance, verbose=False):
        start = self.position
        self.power = power
        end = self.position
        while abs(end - start) < distance:
            if verbose:
                print("position: ", self.position, "end", end)
            end = self.position
            Wait(0.01)

        self.power = 0


def Motors(port_letters, size=None):
    m = []
    ports = [1, 2, 3, 4]  # A=1, B=2, C=3, D=4

    for letter in port_letters:
        i = ord(letter.upper()) - 65
        m.append(Motor(ports[i]))
        
    if len(m) == 0:
        return None
    elif len(m) == 1:
        return m[0]
    else:
        return m


def Shutdown():
    command = {
        "method": "shutdown"
    }
    client = get_client()
    client.send_command(command)
    print("Shutdown.")

def take_picture(filename='picture.jpg', brightness=100, S=10):
    """
    Take a picture using the webcam on the robot.
    The image is captured on the server and transferred to the client.
    
    Args:
        filename: Name of the file to save locally
        brightness: Camera brightness (0-100)
        S: Number of frames to skip before capture
    """
    import base64
    
    client = get_client()
    command = {
        "method": "take_picture",
        "filename": filename,
        "brightness": brightness,
        "S": S
    }
    
    image_b64 = client.send_command(command)
    
    if image_b64:
        # Decode base64
        image_bytes = base64.b64decode(image_b64)
        
        # Check if it's PPM format (offline mode)
        if image_bytes.startswith(b'P6'):
            # Convert PPM to JPG using PIL (only on client side)
            try:
                from PIL import Image
                import io
                img = Image.open(io.BytesIO(image_bytes))
                img.save(filename, 'JPEG')
            except ImportError:
                # If PIL not available, save as PPM
                ppm_filename = filename.replace('.jpg', '.ppm').replace('.jpeg', '.ppm')
                with open(ppm_filename, 'wb') as f:
                    f.write(image_bytes)
                print(f"Picture saved to {ppm_filename} (install PIL to convert to JPEG)")
                return ppm_filename
        else:
            # Real JPEG from camera
            with open(filename, 'wb') as f:
                f.write(image_bytes)
        
        print(f"Picture saved to {filename}")
        return filename
    else:
        print("Failed to capture picture")
        return None