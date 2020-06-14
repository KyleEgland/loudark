# Loudark
Proxy server written in Python 3

## Synopsis

A proxy server for watching network traffic.

## Goals

I. Proxy network traffic
    1. Accept incoming host connection
        a. _TODO:_ What should this be able to handle (e.g. http, https, ftp, ssh, etc.)?
    2. Provide access to traffic for later use (e.g. logging traffic to file, modification, etc.)
    3. Pass traffic (modified or original) to destination
    4. Receive response from destination
    5. Provide access to response for later use
II. Log proxied traffic to file

## Credits

* _[Black Hat Python](https://nostarch.com/blackhatpython)_  by Justin Seitz
* ["Socket Programming in Python (Guide)"](https://realpython.com/python-sockets/#multi-connection-client-and-server) by Nathan Jennings
