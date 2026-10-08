"""
Robot373 ZMQ Server
Runs on the Raspberry Pi and interfaces with the actual BrickPi3 hardware.
Receives commands via ZMQ and executes them using the original robot.py library.
"""

import zmq
import json
import sys
import argparse
import os
import base64

# Import the original robot library
try:
    import brickpi3
    BP = brickpi3.BrickPi3()
    OFFLINE_MODE = False
except ImportError:
    print("Warning: brickpi3 not found. Running in offline mode.")
    BP = None
    OFFLINE_MODE = True

# Storage for initialized sensors and motors
sensors = {}  # port -> sensor object
motors = {}   # port -> motor object


class ServerSensor:
    """Server-side sensor wrapper"""
    def __init__(self, port, sensor_type):
        self.port = port
        self.sensor_type = sensor_type
        
        if not OFFLINE_MODE:
            # Map sensor type strings to BrickPi3 constants
            sensor_type_map = {
                'ir': BP.SENSOR_TYPE.EV3_INFRARED_PROXIMITY,
                'nxtus': BP.SENSOR_TYPE.NXT_ULTRASONIC,
                'us': BP.SENSOR_TYPE.EV3_ULTRASONIC_CM,
                'touch': BP.SENSOR_TYPE.TOUCH,
                'color': BP.SENSOR_TYPE.EV3_COLOR_COLOR_COMPONENTS,
                'gyro': BP.SENSOR_TYPE.EV3_GYRO_ABS_DPS,
            }
            
            bp_sensor_type = sensor_type_map.get(sensor_type)
            if bp_sensor_type:
                BP.set_sensor_type(port, bp_sensor_type)
    
    def get_value(self):
        if not OFFLINE_MODE:
            try:
                return BP.get_sensor(self.port)
            except Exception as error:
                print(f"Sensor error: {error}")
                return None
        else:
            # Offline fake data
            import time
            from math import sin
            t = time.time()
            
            if self.sensor_type in ['ir', 'nxtus', 'us', 'gyro']:
                return int((sin(t / 10 * 2 * 3.14159) + 1) / 2 * 50)
            elif self.sensor_type == 'touch':
                return (sin(t / 10 * 2 * 3.14159) + 1) / 2 > 0.5
            elif self.sensor_type == 'color':
                return [
                    int((sin(t / 10 * 2 * 3.14159) + 1) / 2 * 255),
                    int((sin(t / 15 * 2 * 3.14159) + 1) / 2 * 255),
                    int((sin(t / 7.6 * 2 * 3.14159) + 1) / 2 * 255),
                    100
                ]
            return None


class ServerMotor:
    """Server-side motor wrapper"""
    def __init__(self, port):
        self.port = port
        self._power = 0
        self._position = 0
        
        if not OFFLINE_MODE:
            # Reset encoder position
            BP.offset_motor_encoder(self.port, BP.get_motor_encoder(self.port))
        else:
            import time
            self.start_time = time.time()
            self.last_position = 0
    
    def reset_position(self):
        if not OFFLINE_MODE:
            BP.offset_motor_encoder(self.port, BP.get_motor_encoder(self.port))
        else:
            import time
            self._position = 0
            self.last_position = 0
            self.start_time = time.time()
    
    def set_dps(self, dps):
        if not OFFLINE_MODE:
            BP.set_motor_dps(self.port, dps)
    
    def get_position(self):
        if not OFFLINE_MODE:
            return BP.get_motor_encoder(self.port)
        else:
            import time
            elapsed = time.time() - self.start_time
            return int(self._power / 3 * elapsed + self.last_position)
    
    def set_position(self, pos):
        if not OFFLINE_MODE:
            BP.set_motor_position(self.port, pos)
        else:
            import time
            self.last_position = pos
            self.start_time = time.time()
    
    def set_power(self, power):
        if not OFFLINE_MODE:
            BP.set_motor_power(self.port, power)
        else:
            import time
            self.last_position = self.get_position()
            self.start_time = time.time()
        self._power = power


def get_bp_port(port_num):
    """Convert port number (1-4) to BrickPi3 port constant"""
    if OFFLINE_MODE:
        return port_num
    
    port_map = {
        1: BP.PORT_1,
        2: BP.PORT_2,
        3: BP.PORT_3,
        4: BP.PORT_4
    }
    return port_map.get(port_num, port_num)


def get_bp_motor_port(port_num):
    """Convert port number (1-4 for A-D) to BrickPi3 motor port constant"""
    if OFFLINE_MODE:
        return port_num
    
    port_map = {
        1: BP.PORT_A,
        2: BP.PORT_B,
        3: BP.PORT_C,
        4: BP.PORT_D
    }
    return port_map.get(port_num, port_num)


def handle_command(command):
    """Process a command and return a response"""
    method = command.get("method")
    
    try:

        # Ping command for connection testing
        if method == "ping":
            return {"status": "ok", "value": "pong"}
        # Sensor commands
        elif method == "init_sensor":
            port = get_bp_port(command["port"])
            sensor_type = command["sensor_type"]
            sensors[port] = ServerSensor(port, sensor_type)
            return {"status": "ok", "value": None}
        
        elif method == "get_sensor_value":
            port = get_bp_port(command["port"])
            if port in sensors:
                value = sensors[port].get_value()
                return {"status": "ok", "value": value}
            else:
                return {"status": "error", "message": f"Sensor on port {port} not initialized"}
        
        # Motor commands
        elif method == "init_motor":
            port = get_bp_motor_port(command["port"])
            motors[port] = ServerMotor(port)
            return {"status": "ok", "value": None}
        
        elif method == "reset_motor_position":
            port = get_bp_motor_port(command["port"])
            if port in motors:
                motors[port].reset_position()
                return {"status": "ok", "value": None}
            else:
                return {"status": "error", "message": f"Motor on port {port} not initialized"}
        
        elif method == "set_motor_dps":
            port = get_bp_motor_port(command["port"])
            dps = command["dps"]
            if port in motors:
                motors[port].set_dps(dps)
                return {"status": "ok", "value": None}
            else:
                return {"status": "error", "message": f"Motor on port {port} not initialized"}
        
        elif method == "get_motor_position":
            port = get_bp_motor_port(command["port"])
            if port in motors:
                position = motors[port].get_position()
                return {"status": "ok", "value": position}
            else:
                return {"status": "error", "message": f"Motor on port {port} not initialized"}
        
        elif method == "set_motor_position":
            port = get_bp_motor_port(command["port"])
            position = command["position"]
            if port in motors:
                motors[port].set_position(position)
                return {"status": "ok", "value": None}
            else:
                return {"status": "error", "message": f"Motor on port {port} not initialized"}
        
        elif method == "set_motor_power":
            port = get_bp_motor_port(command["port"])
            power = command["power"]
            if port in motors:
                motors[port].set_power(power)
                return {"status": "ok", "value": None}
            else:
                return {"status": "error", "message": f"Motor on port {port} not initialized"}
        
        # Utility commands
        elif method == "shutdown":
            if not OFFLINE_MODE:
                BP.reset_all()
            return {"status": "ok", "value": None}
        

        elif method == "take_picture":
            
            filename = command.get("filename", "picture.jpg")
            brightness = command.get("brightness", 100)
            S = command.get("S", 10)
            
            if not OFFLINE_MODE:
                # Take real picture
                cmd = f"fswebcam -s brightness={brightness}%% -r 1600x900 --no-banner -S {S} '{filename}'"
                result = os.system(cmd)
                
                if result == 0 and os.path.exists(filename):
                    # Read the image file and encode as base64
                    with open(filename, 'rb') as f:
                        image_bytes = f.read()
                    image_b64 = base64.b64encode(image_bytes).decode('utf-8')
                    os.remove(filename)  # Clean up server-side file
                    return {"status": "ok", "value": image_b64}
                else:
                    return {"status": "error", "message": "Failed to capture image"}

            else:
                # Offline mode - create a 500x500 random static image in PPM format
                import random
            
                width, height = 500, 500
                ppm_data = f"P6\n{width} {height}\n255\n"
            
                # Generate random RGB pixels
                pixel_data = bytes([random.randint(0, 255) for _ in range(width * height * 3)])
            
                # Combine header and pixel data
                image_bytes = ppm_data.encode('ascii') + pixel_data
            
                # Convert to base64
                image_b64 = base64.b64encode(image_bytes).decode('utf-8')
                return {"status": "ok", "value": image_b64}            
            
    
    except Exception as e:
        return {"status": "error", "message": str(e)}


def main():
    """Main server loop"""
    global VERBOSE
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Robot373 ZMQ Server')
    parser.add_argument('--verbose', '-v', default=True,
                        type=lambda x: (str(x).lower() in ['true', '1', 'yes']),
                        help='Enable verbose output (default: True)')    
    parser.add_argument('--port', '-p', type=int, default=5555,
                        help='Port to listen on (default: 5555)')
    args = parser.parse_args()
    
    VERBOSE = args.verbose
    port = args.port
    
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{port}")
    
    print(f"Robot373 ZMQ Server started on port {port}")
    if OFFLINE_MODE:
        print("Running in OFFLINE mode (no BrickPi3 hardware)")
    else:
        print("Connected to BrickPi3 hardware")
    
    if VERBOSE:
        print("VERBOSE mode: ON")
    
    print("Waiting for commands...")
    print()


    try:
        while True:
            # Wait for command
            message = socket.recv_json()
            
            if VERBOSE:
                # Don't print full image data in take_picture responses
                if message.get("method") == "take_picture":
                    print(f"[CLIENT → SERVER] {{'method': 'take_picture', 'filename': '{message.get('filename')}', ...}}")
                else:
                    print(f"[CLIENT → SERVER] {message}")
            
            # Process command
            response = handle_command(message)
            
            if VERBOSE:
                # Don't print full base64 image data
                if message.get("method") == "take_picture" and response.get("status") == "ok":
                    img_size = len(response.get("value", ""))
                    print(f"[SERVER → CLIENT] {{'status': 'ok', 'value': '<image data {img_size} bytes>'}}")
                else:
                    print(f"[SERVER → CLIENT] {response}")
                print()  # Blank line for readability
            
            # Send response
            socket.send_json(response)

    
    except KeyboardInterrupt:
        print("\nShutting down server...")
        if not OFFLINE_MODE:
            BP.reset_all()
    
    finally:
        socket.close()
        context.term()


if __name__ == "__main__":
    main()
