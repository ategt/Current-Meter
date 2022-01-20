from random import randint
from time import sleep
import threading
import socketio
import time
import re

DATA_REGEX = re.compile(r"(?P<currentSpeedKmh>[0-9\.]+)\,(?P<currentAccelMss>[0-9\.\-]+)\,(?P<currentRevsPerMin>[0-9\.]+)\,(?P<totalDistanceMetres>[0-9\.]+)\,(?P<totalTimeSeconds>[0-9\.]+)\,(?P<tripDistanceMetres>[0-9\.]+)\,(?P<tripTimeSeconds>[0-9\.]+)\,(?P<tripMaxSpeedKmh>[0-9\.]+)")
LINE_REGEX = re.compile(r"(?P<timestamp>[0-9\.]+)\,(?P<currentSpeedKmh>[0-9\.]+)\,(?P<currentAccelMss>[0-9\.\-]+)\,(?P<currentRevsPerMin>[0-9\.]+)\,(?P<totalDistanceMetres>[0-9\.]+)\,(?P<totalTimeSeconds>[0-9\.]+)\,(?P<tripDistanceMetres>[0-9\.]+)\,(?P<tripTimeSeconds>[0-9\.]+)\,(?P<tripMaxSpeedKmh>[0-9\.]+)")

def read(path):
    with open(path, 'rb') as handle:
        try:
            return handle.read().decode("utf-8")
        except UnicodeDecodeError:
            return ""

def main():        
    data = read("../data/speed-log.txt")
    lines = data.split("\r\n")

    sio = socketio.Client()
    event = threading.Event()
    
    @sio.on("recorder directive broadcast")
    def directive_handler(data):
        if data['directive'] == 'shutdown':
            sio.emit("recorder action", {"data":"Shutdown Order Received"})
            event.set()
        else:
            sio.emit("recorder action", {"message":"Unknown Request Received", "data":data})

    uri = "ws://127.0.0.1:5000/"
    backward_readings = reversed([LINE_REGEX.search(line).groupdict() for line in lines if LINE_REGEX.search(line)])

    try:
        if sio:
            sio.connect(uri)
            
        for result in backward_readings:
            try:
                sio.emit("speedometer update", {"data":result})
                if event.is_set():
                    quit(0)

            except socketio.exceptions.BadNamespaceError as ex:
                pass
            
            print("\r", result['currentRevsPerMin'], " - ", randint(0, 250), " " * 25, end='')
            sleep(0.9)

    except KeyboardInterrupt:
        print("")
        quit(0)
    finally:
        sio.disconnect()

if __name__ == '__main__':
    main()