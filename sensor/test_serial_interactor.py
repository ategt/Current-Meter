import unittest

from .serial_interactor import SensorMonitor
from time import sleep

class TestSpeedometer(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_speedometer(self):
        """ 
            The Arduino module explained in the readme file
            must be connected for this test to pass.
        """
        sensorMonitor = SensorMonitor("COM4", 9600)
        sensorMonitor.writeConfig( 60,-1.37,0.037689,120,1,5000 )
        sensorMonitor.writeConfig( 60,-1.37,0.037689,120,1,5000 )
        sensorMonitor.getData()
        sensorMonitor.getConfig()
        sensorMonitor.close()

if __name__ == '__main__':
    unittest.main()