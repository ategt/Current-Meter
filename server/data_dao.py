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

    def _readFileOffset(self, fileName, offset, limit = None):
        filePath = os.path.join(self.dataPath, fileName)
        #fileSize = os.stat(filePath).st_size

        hint = -1 if limit is None else limit

        with open(filePath, 'r') as handle:
            handle.seek(offset)
            return handle.readlines(hint)
            # lines = handle.readlines(hint)         
            # print(f"{offset}x{limit} H={hint} : {lines}")
            # return lines

    def getData(self, fileName):
        content = self.readFile(fileName)
        return [self._parseLine(line) for line in content.strip().split("\n")]

    def _parseLine(self, line):
        initial_datum = self.DATA_LINE_REGEX.match(line).groupdict()

        datum = dict((key, value) for key, value in initial_datum.items() if value is not None)

        for key, value in datum.items():
            if self.INTEGER_REGEX.match(value):
                datum[key] = int(value)
            elif self.FLOAT_REGEX.match(value):
                datum[key] = float(value)

        return datum

    def _getTimecode(self, line):
        match = self.DATA_LINE_REGEX.match(line).groupdict()
        return float(match['timecode'])

    def getTimes(self, fileName, start, end):
        if start > end:
            raise Exception("Start time must occurr before end time!")

        content = self.readFile(fileName)
        lines = content.strip().split("\n")

        return [self._parseLine(line) for line in lines if self._getTimecode(line) > start and self._getTimecode(line) < end]

    def determineOffset(self, fileName, timecode):
        filePath = os.path.join(self.dataPath, fileName)

        with open(filePath, 'r') as handle:
            handle.seek(0)

            line = -1

            while line != "":
                line = handle.readline()
                line_timecode = self._getTimecode(line)

                if line_timecode == timecode:
                    ending_position = handle.tell() - 1
                    starting_position = ending_position - len(line)
                    trimmed_ending_position = starting_position + len(line.strip())

                    return {"start": starting_position, "end": trimmed_ending_position, "limit": trimmed_ending_position - starting_position}

    def getOffset(self, fileName, offset, limit):
        lines = self._readFileOffset(fileName = fileName, offset = offset, limit = limit)
        return [self._parseLine(line.strip()) for line in lines]