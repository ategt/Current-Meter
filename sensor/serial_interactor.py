# coding: utf-8

from random import randint
from time import sleep
import serial
import re

class SensorMonitor(object):
    """SensorMonitor object for use with Arduino companion project

        Examples:
        sensorMonitor = SensorMonitor("COM4", 9600)
        sensorMonitor.writeConfig( 60,-1.37,0.037689,120,1,5000 )
        sensorMonitor.getData()
        sensorMonitor.getConfig()

        for _ in range(90):
            result = sensorMonitor.getData()
            print("\r", result['watts'], " - ", randint(0, 250), end='')
            sleep(0.9)
    """
    def __init__(self, port, baudrate):
        super(SensorMonitor, self).__init__()
        self.DATA_REGEX = re.compile(r"Reading\: (?P<reading>[0-9\.\-]+)\t Adjusted: (?P<adjustedReading>[0-9\.\-]+)\t Amps: (?P<amps>[0-9\.\-]+)\t Watts: (?P<watts>[0-9\.\-]+)")
        self.DATA_TEMP_REGEX = re.compile(r"Reading\: (?P<reading>[0-9\.\-]+)\t Adjusted: (?P<adjustedReading>[0-9\.\-]+)\t Amps: (?P<amps>[0-9\.\-]+)\t Watts: (?P<watts>[0-9\.\-]+)\,(?P<instant_temperature>[0-9]+)\,(?P<denoised_temperature_reading>[0-9]+)\,(?P<instant_exterior_temperature>[0-9]+)\,(?P<denoised_exterior_temperature_reading>[0-9]+)\,(?P<instant_frige_temperature>[0-9]+)\,(?P<denoised_frige_temperature_reading>[0-9]+)")
        self.CONFIG_REGEX = re.compile(r"(?P<frequency>[0-9\.]+)\,(?P<intercept>[0-9\.\-]+)\,(?P<slope>[0-9\.\-]+)\,(?P<voltage>[0-9\.\-]+)\,(?P<windowLength>[0-9\.\-]+)\,(?P<printPeriod>[0-9\.\-]+)")
        self.WAITING_REGEX = re.compile(r"\.\.\.pausing for (?P<delay>[0-9]+) milliseconds")
        self.READING_REGEX = re.compile(r"(?P<millis>[0-9]+)\,(?P<hall_reading>[0-9]+)")
        self.TEMPERATURE_REGEX = re.compile(r"(?P<instant_temperature>[0-9]+)\,(?P<denoised_temperature_reading>[0-9]+)")

        self.port = port
        self.baudrate = baudrate

        self._serial = serial.Serial(self.port, self.baudrate)

        sleep(2)

        print("connected to: " + self._serial.portstr)

    def getData(self):
        _ = self._serial.write(b"readdata\n\r")

        self.line = self._serial.readline()
        response = self.line.decode("utf-8").strip()
        
        return self.DATA_TEMP_REGEX.search(response).groupdict()

    def getRawData(self):
        _ = self._serial.write(b"readraw\n\r")
        
        self.line = self._serial.readline()
        response = self.line.decode("utf-8").strip()

        values = response.split(",")

        return {"start": values[0], "end": values[-1], "readings": values[1:-1]}

    def _getTemperatureReading(self):
        self.line = self._serial.readline()
        response = self.line.decode("utf-8").strip()
        
        return self.TEMPERATURE_REGEX.search(response).groupdict()

    def getWaveData(self, logger = None):
        _ = self._serial.write(b"readdelay\n\r")
        
        self.line = self._serial.readline()
        response = self.line.decode("utf-8").strip()

        try:
            return self.READING_REGEX.search(response).groupdict()
        except:
            delay = int(self.WAITING_REGEX.search(response).groupdict()['delay'])

            if logger:
                logger(delay)

            sleep(delay/1000+5)

            self.line = self._serial.readline()
            response = self.line.decode("utf-8").strip()

            return self.READING_REGEX.search(response).groupdict()

    def resetConfig(self):
        _ = self._serial.write(b"rstconf\n\r")
        
        line = self._serial.readline()
        response = line.decode("utf-8").strip()
       
        return response == 'ok'

    def getConfig(self):
        _ = self._serial.write(b"readconf\n\r")
        
        line = self._serial.readline()
        response = line.decode("utf-8").strip()
       
        return self.CONFIG_REGEX.search(response).groupdict()

    def writeConfig(self, frequency, intercept, slope, voltage, windowLength, printPeriod):
        _ = self._serial.write("writeconf {},{},{},{},{},{}\n\r".format(frequency, intercept, slope, voltage, windowLength, printPeriod).encode())
        
        line = self._serial.readline()
        response = line.decode("utf-8").strip()
       
        return response == 'ok'

    def getLastLine(self):
        return self.line

    def close(self):
        return self._serial.close()