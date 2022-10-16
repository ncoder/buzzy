#!/usr/bin/env python3
"""
This code allows you to serve static files from the same port as the websocket connection

This is only suitable for small files and as a development server!
open(full_path, 'rb').read() call that is used to send files will block the whole asyncio loop!
"""

import asyncio
import functools
import os
from http import HTTPStatus

import websockets

from remote_control import opmap

MIME_TYPES = {"html": "text/html", "js": "text/javascript", "css": "text/css"}


async def process_request(sever_root, path, request_headers):
    """Serves a file when doing a GET request with a valid path."""

    if "Upgrade" in request_headers:
        return  # Probably a WebSocket connection

    if path == '/':
        path = '/index.html'

    response_headers = [
        ('Server', 'asyncio websocket server'),
        ('Connection', 'close'),
    ]

    # Derive full system path
    full_path = os.path.realpath(os.path.join(sever_root, path[1:]))

    # Validate the path
    if os.path.commonpath((sever_root, full_path)) != sever_root or \
            not os.path.exists(full_path) or not os.path.isfile(full_path):
        print("HTTP GET {} 404 NOT FOUND".format(path))
        return HTTPStatus.NOT_FOUND, [], b'404 NOT FOUND'

    # Guess file content type
    extension = full_path.split(".")[-1]
    mime_type = MIME_TYPES.get(extension, "application/octet-stream")
    response_headers.append(('Content-Type', mime_type))

    # Read the whole file into memory and send it out
    body = open(full_path, 'rb').read()
    response_headers.append(('Content-Length', str(len(body))))
    print("HTTP GET {} 200 OK".format(path))
    return HTTPStatus.OK, response_headers, body


async def control(websocket, path):
    print("New WebSocket connection from", websocket.remote_address)
    await websocket.send("Welcome " + str(websocket.remote_address))
    while websocket.open:
        message = await websocket.recv()
        if isinstance(message, str):
            await websocket.send(message)
        elif isinstance(message, bytes):
            opcode = message[0]
            if opcode in opmap:
                opmap[opcode]()
            else:
                await websocket.send("unrecognized opcode: " + str(opcode))
        else:
            await websocket.send("unknown type")

    # This print will not run when abrnomal websocket close happens
    # for example when tcp connection dies and no websocket close frame is sent
    print("WebSocket connection closed for", websocket.remote_address)


# call this with asyncio.get_event_loop().run_until_complete(listenForRemoteInput)
# to process external input events.
async def listenForRemoteInput():
    # set first argument for the handler to current working directory
    handler = functools.partial(process_request,
                                os.path.join(os.getcwd(), "www"))
    await websockets.serve(control, None, 8080, process_request=handler)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(listenForRemoteInput())
    asyncio.get_event_loop().run_forever()
