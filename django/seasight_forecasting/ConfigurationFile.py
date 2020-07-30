
import configparser
from seasight_forecasting import global_vars

def CheckConfigFile():
    pass
    

def LoadConfigFile():
    config = configparser.ConfigParser()
    configFilePath = r'app.conf'
    config.read(configFilePath)
    
    global_vars.historic_file_path = config['FILES']['historic_data_path'] + config['FILES']['historic_data_file']
    global_vars.prediction_model_path = config['FILES']['prediction_model_path'] + config['FILES']['prediction_model_file']
    global_vars.north_atlantic_region_path = config['FILES']['regions_path'] + config['FILES']['north_atlantic_region_file']
    global_vars.south_atlantic_region_path = config['FILES']['regions_path'] + config['FILES']['south_atlantic_region_file']
    global_vars.indian_region_path = config['FILES']['regions_path'] + config['FILES']['indian_region_file']
    global_vars.west_pacific_region_path = config['FILES']['regions_path'] + config['FILES']['west_pacific_region_file']
    global_vars.east_pacific_region_path = config['FILES']['regions_path'] + config['FILES']['east_pacific_region_file']
    global_vars.kml_destination = config['FILES']['kml_destination_path'] + config['FILES']['kml_destination_file']

    global_vars.number_of_clusters = int(config['KML']['number_of_clusters'])
    
    print('Global variables loaded!')
