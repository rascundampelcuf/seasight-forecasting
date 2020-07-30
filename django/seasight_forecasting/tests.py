import configparser
import os
import pytest
import unittest


class TestConfigFile(unittest.TestCase):
    
    def test_config_file_exists(self):
        self.assertTrue(os.path.isfile('app.conf'))
        
    def test_config_file_not_empty(self):
        self.assertGreater(os.stat('app.conf').st_size, 0)

class TestConfigFileContent(unittest.TestCase):
    
    config = configparser.ConfigParser()
    configFilePath = r'app.conf'
    config.read(configFilePath)
    pytest.config = config
    
    def test_historic_file_exists(self):
        path = pytest.config['FILES']['historic_data_path']
        file = pytest.config['FILES']['historic_data_file']
        self.assertTrue(os.path.isfile(path + file))
        
    def test_prediction_model_file_exists(self):
        path = pytest.config['FILES']['prediction_model_path']
        file = pytest.config['FILES']['prediction_model_file']
        self.assertTrue(os.path.isfile(path + file))
        
    def test_regions_files_exists(self):
        path = pytest.config['FILES']['regions_path']
        na = pytest.config['FILES']['north_atlantic_region_file']
        sa = pytest.config['FILES']['south_atlantic_region_file']
        i = pytest.config['FILES']['indian_region_file']
        wp = pytest.config['FILES']['west_pacific_region_file']
        ep = pytest.config['FILES']['east_pacific_region_file']
        self.assertTrue(os.path.isfile(path + na))
        self.assertTrue(os.path.isfile(path + sa))
        self.assertTrue(os.path.isfile(path + i))
        self.assertTrue(os.path.isfile(path + wp))
        self.assertTrue(os.path.isfile(path + ep))
        
    def test_kml_destination_path_exists(self):
        path = pytest.config['FILES']['kml_destination_path']
        self.assertTrue(os.path.isdir(path))
        
    def test_number_of_clusters_is_correct(self):
        n_clusters = int(pytest.config['KML']['number_of_clusters'])
        self.assertGreater(n_clusters, 0)

if __name__ == '__main__':
    unittest.main()