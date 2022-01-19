# coding: utf-8

from datetime import datetime
from random import randint
from time import sleep
import socketio
import serial
import time
import re
import os

def main():
  try:
    _serial = serial.Serial("COM4", 9600)
    sio = socketio.Client()
    comma = ",".encode()
    
    result = _serial.read_all()
    
    with open(os.path.join(os.getenv("DATA_PATH"), "temp.txt"), 'ab') as handle:
        handle.write(str(time.time()).encode())
        handle.write(comma)
        handle.write(result)
    
    if sio:
        sio.connect("ws://127.0.0.1:5000/")

    date_string = datetime.now().strftime("%F")

    with open(os.path.join(os.getenv("DATA_PATH"), f"temp-{date_string}.txt"), 'ab') as handle:
      for _ in range(90000):
              result = _serial.readline()
              handle.write(str(time.time()).encode())
              handle.write(comma)
              handle.write(result)

              readings = result.split(comma)
              first_reading = readings[0]
              avg_reading = readings[-1]

              try:
                  sio.emit("sensor reading event", {"data":str(avg_reading)})
              except socketio.exceptions.BadNamespaceError as ex:
                  pass
              
              print("\r", first_reading.decode("utf-8"), ",", avg_reading.decode("utf-8").strip(), " - ", randint(0, 250), " " * 25, end='')
              sleep(0.5)
  finally:            
    _serial.close()
    sio.disconnect()

if __name__ == "__main__":
  main()