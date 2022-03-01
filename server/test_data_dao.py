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

    def test_getOffset(self):
        files = self.dataDao.listFiles()

        for file in files:
            print("Get Offset -", file)
            
            data = self.dataDao.getData(file)
            record_count = len(data)
            index = random.randint(0, record_count)
            selected_record = data[index]
            timecode = selected_record['timecode']
            offset_meta = self.dataDao.determineOffset(file, timecode)

            returned_data = self.dataDao.getOffset(file, offset = offset_meta['start'], limit = offset_meta['end'] - offset_meta['start'])

            self.assertEqual(len(returned_data), 1, "Using the specified offset should return only one record. {}, limit:{}".format(offset_meta, offset_meta['end'] - offset_meta['start']))

            datum = returned_data[0]

            self.assertEqual(set(datum.keys()), set(selected_record.keys()))
            
            for key in datum.keys():
                self.assertEqual(datum[key], selected_record[key])

            returned_data_pair = self.dataDao.getOffset(file, offset = offset_meta['start'], limit = offset_meta['end'] - offset_meta['start'] + 2)

            self.assertEqual(len(returned_data_pair), 2, "Using the specified offset should return two records.")

            paired_datum = returned_data_pair[0]
            extra_record = returned_data_pair[1]

            self.assertEqual(set(datum.keys()), set(paired_datum.keys()))
            self.assertEqual(set(datum.keys()), set(extra_record.keys()), "This check seemed worth doing, but it may fail and the program would still work.")
            
            for key in paired_datum.keys():
                self.assertEqual(datum[key], paired_datum[key])

if __name__ == '__main__':
    unittest.main()