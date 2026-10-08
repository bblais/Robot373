#!/usr/bin/env python
"""
Robot373 ZMQ Server - Module entry point

Allows running the server with:
    python -m Robot373.zmq.server --verbose True --port 5555
"""

from .server import main

if __name__ == "__main__":
    main()

    