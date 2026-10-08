"""
Robot373 ZMQ Submodule
Provides remote robot control over network using ZeroMQ.

Client side usage:
    from Robot373.zmq import *
    setup_client('192.168.1.100:5555')
    left, right = Motors("ab")
    left.power = 30

Server side usage:
    from Robot373.zmq import run_zmq_server
    run_zmq_server(verbose=True, port=5555)
"""

# Import all client functions and classes
from .client import (
    # Core functions
    setup_client,
    get_client,
    set_verbose,
    Wait,
    Shutdown,
    take_picture,

    # Classes
    ZMQClient,
    Sensor,
    Motor,
    Timer,

    # Factory functions
    Sensors,
    Motors,
    warm_up_sensors,

    # Utility functions
    closest_color,
    closest_color_as_number,
)

# Import server module for direct access if needed
from . import server

# Server convenience function
def run_zmq_server(verbose=True, port=5555):
    """
    Run the ZMQ server on the Raspberry Pi.

    Args:
        verbose: Enable verbose output (default: True)
        port: Port to listen on (default: 5555)

    Example:
        from Robot373.zmq import run_zmq_server
        run_zmq_server(verbose=True, port=5555)
    """
    import sys

    # Set up arguments for the server
    sys.argv = ['server', '--verbose', str(verbose), '--port', str(port)]

    # Run the server
    server.main()


__all__ = [
    # Client functions
    'setup_client',
    'get_client',
    'set_verbose',
    'Wait',
    'Shutdown',
    'take_picture',

    # Classes
    'ZMQClient',
    'Sensor',
    'Motor',
    'Timer',

    # Factory functions
    'Sensors',
    'Motors',
    'warm_up_sensors',

    # Utility functions
    'closest_color',
    'closest_color_as_number',

    # Server function
    'run_zmq_server',
]