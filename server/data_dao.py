import re
import os


class DataDao(object):
    """docstring for DataDao"""
    def __init__(self, dataPath):
        super(DataDao, self).__init__()
        self.dataPath = dataPath
        self.DATA_LINE_REGEX = re.compile(r"(?:1643495056\.2245536\,)?(?P<timecode>[0-9\.]+)\,\t\s+Reading\: (?P<reading>[0-9\.\-]+)\t Adjusted: (?P<adjustedReading>[0-9\.\-]+)\t Amps: (?P<amps>[0-9\.\-]+)\t Watts: (?P<watts>[0-9\.\-]+)\,(?P<instant_temperature>[0-9]+)\,(?P<denoised_temperature_reading>[0-9]+)(\,(?P<instant_exterior_temperature>[0-9]+)\,(?P<denoised_exterior_temperature_reading>[0-9]+)(\,(?P<instant_frige_temperature>[0-9]+)\,(?P<denoised_frige_temperature_reading>[0-9]+))??)??")
        self.INTEGER_REGEX = re.compile(r"\A[0-9\-]+\Z")
        self.FLOAT_REGEX = re.compile(r"\A[0-9\-\.]+\Z")

    def listFiles(self):
        return os.listdir(self.dataPath)

    def readFile(self, fileName):
        filePath = os.path.join(self.dataPath, fileName)

        with open(filePath, 'r') as handle:
            return handle.read()

    def getData(self, fileName):
        content = self.readFile(fileName)
        return [self._parseLine(line) for line in content.strip().split("\n")]

    def _parseLine(self, line):
        initial_datum = self.DATA_LINE_REGEX.match(line).groupdict()

        datum = dict((key, value) for key, value in initial_datum.items() if value is not None)

        for key, value in datum.items():
            if value is None:
                _ = datum.pop(key)
            if self.INTEGER_REGEX.match(value):
                datum[key] = int(value)
            elif self.FLOAT_REGEX.match(value):
                datum[key] = float(value)

        return datum

    def getTimes(self, fileName, start, end):
        if start > end:
            raise Exception("Start time must occurr before end time!")

        data = self.getData(fileName)

        return [datum for datum in data if float(datum['timecode']) > start and float(datum['timecode']) < end]
