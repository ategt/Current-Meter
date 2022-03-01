# coding: utf-8

from serial_interactor import SensorMonitor
from datetime import datetime
from random import randint
from time import sleep
import socketio
import time
import re
import os

def minimum_run():
    try:
        sensorMonitor = SensorMonitor("COM4", 9600)
        sio = socketio.Client()
        comma = ",".encode()

        if sio:
            sio.connect("ws://127.0.0.1:5000/")

        date_string = datetime.now().strftime("%F")

        with open(os.path.join(os.getenv("DATA_PATH"), f"fridge-{date_string}.txt"), 'ab') as handle:
            for _ in range(360):
                data_result = sensorMonitor.getData()
                handle.write(str(time.time()).encode())
                handle.write(comma)
                handle.write(_sensorMonitor.getLastLine())

                try:
                    sio.emit("board response event", {"data":data_result})
                except socketio.exceptions.BadNamespaceError as ex:
                    pass

                print("\r", data_result['denoised_temperature_reading'], ",", data_result['watts'], " - ", randint(0, 250), " " * 25, end='')
                sleep(0.1)
    finally:            
        _sensorMonitor.close()
        sio.disconnect()

def main():
    for i in range(48):
        print(f"Beginning Segment {i}")
        minimum_run()
        sleep(10)

if __name__ == "__main__":
    main()