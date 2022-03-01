import unittest
import random
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
            print("Get Data -", file)
            data = self.dataDao.getData(file)
            self.assertTrue(len(data) > 1, file)

    def test_getTimeData(self):
        files = self.dataDao.listFiles()

        for file in files:
            print("Get Times -", file)
            data = self.dataDao.getData(file)
            all_data = self.dataDao.getTimes(file, -float("inf"), float("inf"))

            self.assertEqual(len(data), len(all_data))

            record_count = len(all_data)

            if record_count > 10:
                start_index = random.randint(1, record_count - 5)
                end_index = random.randint(start_index, record_count - 1)

                sub_data = self.dataDao.getTimes(file, data[start_index]['timecode'], data[end_index]['timecode'])

                self.assertTrue(len(sub_data) <= record_count - 2)

if __name__ == '__main__':
    unittest.main()