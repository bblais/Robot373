#!/usr/bin/env python
"""
Robot373 ZMQ Server Launcher Script

This script provides an easy way to start the Robot373 ZMQ server.

Usage:
    python run_zmq_server.py
    python run_zmq_server.py --verbose True --port 5555
    python run_zmq_server.py -v False -p 6000
"""

from Robot373.zmq import run_zmq_server
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Robot373 ZMQ Server Launcher')
    parser.add_argument('--verbose', '-v', default=True,
                        type=lambda x: (str(x).lower() in ['true', '1', 'yes']),
                        help='Enable verbose output (default: True)')
    parser.add_argument('--port', '-p', type=int, default=5555,
                        help='Port to listen on (default: 5555)')
    args = parser.parse_args()

    run_zmq_server(verbose=args.verbose, port=args.port)
