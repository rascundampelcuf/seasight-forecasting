import unittest
import pandas as pd
import pytest

from seasight_forecasting.ManageData import *

class TestDateRange(unittest.TestCase):

    pytest.data = pd.DataFrame(data={'time': [
        '2020-07-24 12:00:00', '2020-07-25 12:00:00',
        '2020-07-26 12:00:00', '2020-07-27 12:00:00',
        '2020-07-28 12:00:00']})

    pytest.dateFrom = '2020-07-25'
    pytest.dateTo = '2020-07-27'

    def test_only_date_from(self):
        data = GetDataInDateRange(pytest.data, pytest.dateFrom, False, None)
        self.assertEqual(data.time.min(), '2020-07-25 12:00:00')
        self.assertEqual(data.time.max(), '2020-07-28 12:00:00')

    def test_date_from_and_date_to(self):
        data = GetDataInDateRange(pytest.data, pytest.dateFrom, True, pytest.dateTo)
        self.assertEqual(data.time.min(), '2020-07-25 12:00:00')
        self.assertEqual(data.time.max(), '2020-07-27 12:00:00')

if __name__ == '__main__':
    unittest.main()