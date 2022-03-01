import re
import os


class DataDao(object):
    """docstring for DataDao"""
    def __init__(self, dataPath):
        super(DataDao, self).__init__()
        self.dataPath = dataPath
        self.DATA_LINE_REGEX = re.compile(r"(?:1643495056\.2245536\,)?(?P<timecode>[0-9\.]+)\,\t\s+Reading\: (?P<reading>[0-9\.\-]+)\t Adjusted: (?P<adjustedReading>[0-9\.\-]+)\t Amps: (?P<amps>[0-9\.\-]+)\t Watts: (?P<watts>[0-9\.\-]+)\,(?P<instant_temperature>[0-9]+)\,(?P<denoised_temperature_reading>[0-9]+)(\,(?P<instant_exterior_temperature>[0-9]+)\,(?P<denoised_exterior_temperature_reading>[0-9]+)\,(?P<instant_frige_temperature>[0-9]+)\,(?P<denoised_frige_temperature_reading>[0-9]+))?")

    def listFiles(self):
        return os.listdir(self.dataPath)

    def readFile(self, fileName):
        filePath = os.path.join(self.dataPath, fileName)

        with open(filePath, 'r') as handle:
            return handle.read()

    def getData(self, fileName):
        content = self.readFile(fileName)
        return [self.DATA_LINE_REGEX.match(line).groupdict() for line in content.strip().split("\n")]

    def getTimes(self, fileName, start, end):
        if start > end:
            raise Exception("Start time must occurr before end time!")

        data = self.getData(fileName)

        return [datum for datum in data if float(datum['timecode']) > start and float(datum['timecode']) < end]
