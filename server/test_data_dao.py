import unittest
import os

from .data_dao import DataDao

class TestDataDao(unittest.TestCase):
    def setUp(self):
        os.environ['DATA_PATH'] = os.path.join("data")
        self.dataDao = DataDao(os.environ['DATA_PATH'])

    def tearDown(self):
        pass

    def test_listFiles(self):
        files = self.dataDao.listFiles()
        self.assertTrue(len(files) > 1)

    def test_readFile(self):
        files = self.dataDao.listFiles()

        for file in files:
            content = self.dataDao.readFile(file)
            self.assertTrue(len(content) > 1)

    def test_getData(self):
        files = self.dataDao.listFiles()

        for file in files:
            print(file)
            data = self.dataDao.getData(file)
            self.assertTrue(len(data) > 1, file)

if __name__ == '__main__':
    unittest.main()