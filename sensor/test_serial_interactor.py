import unittest

from .serial_interactor import SensorMonitor
from time import sleep

class TestSensorMonitor(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sensorMonitor(self):
        """ 
            The Arduino module explained in the readme file
            must be connected for this test to pass.
        """
        sensorMonitor = SensorMonitor("COM4", 9600)

        cfg = sensorMonitor.getConfig()
        self.validateConfig(cfg)

        sensorMonitor.writeConfig( 60,-1.37,0.037689,120,1,5000 )
        sensorMonitor.writeConfig( 60,-1.37,0.037689,120,1,5000 )

        cfg = sensorMonitor.getConfig()
        self.validateConfig(cfg)

        sensorMonitor.getData()
        sensorMonitor.getRawData()
        sensorMonitor.getWaveData()

        cfg = sensorMonitor.getConfig()
        self.validateConfig(cfg)

        sensorMonitor.resetConfig()
        cfg = sensorMonitor.getConfig()
        self.validateConfig(cfg)

        sensorMonitor.getLastLine()
        sensorMonitor.close()

    def validateConfig(self, config):
        keys = ['frequency', 'intercept', 'printPeriod', 'slope', 'voltage', 'windowLength']

        for key in keys:
            self.assertTrue(key in config.keys(), f"{key} was not found in config: {config}")

if __name__ == '__main__':
    unittest.main()