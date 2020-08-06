# Seasight-Forecasting

## __Google Summer Of Code 2020__
<p align="center"> 
    <img width="600" src="https://jderobot.github.io/assets/images/activities/gsoc-2020.jpg">
</p>

__Welcome to Seasight Forecasting project__

This project is developed in a context of a scolarship in the program Google Summer Of Code 2020 and is a web application based on Django that pretends to display on the Liquid Galaxy sea surface temperatures based on 3 use cases: display historic temperatures, display real time temperatures and display predicted temperatures.

<p align="center"> 
 <img width="200" src="django/seasight_forecasting/static/seasight_forecasting/logos/SF-logo.png">
</p>

## Source files

The application runs in a Django environment, so the files that are part of its structure will not be listed.

Below are the files that contain the core of the application and the functions needed for it to work properly

```bash
────Seasight-Forecasting
    │   .cdsapirc
    │
    ├───data
    │   │   historic.csv
    │   │
    │   └───regions
    │           east_pacific.geojson
    │           indian.geojson
    │           north_atlantic.geojson
    │           south_atlantic.geojson
    │           west_pacific.geojson
    │
    └───django
        │   app.conf
        │   requirements.txt
        │
        └───seasight_forecasting
                CaseMethods.py
                Clustering.py
                ConfigurationFile.py
                GenerateKML.py
                global_vars.py
                ManageData.py
                ManageModel.py
                tests.py
```
- **.cdsapirc**: API credentials file. Contains the credentials that enable communication between the application and the API.
- **data/historic.csv**: File that contains historical data that is used by the "Historic" section of the application.
- **data/regions/*.geojson**: List of geojson files that contains the polygon coordinates of the different ocean regions.
- **django/app.conf**: Configuration file with customizable parameters. The parameters of this file are described below.
- **django/requirements.txt**: File with the required packages for the application to work properly. 
- **django/seasight_forecasting/CaseMethods.py**: This file contains the main methods for the different cases (Historic, Real-time, Future).
- **django/seasight_forecasting/Clustering.py**: This file contains the methods to group the data and obtain the coordinates of the polygons in these groups. In addition to the methods to obtain the colormap and the colors of the regions.
- **django/seasight_forecasting/ConfigurationFile.py**: This file contains the initialization of the configuration file by dumping its content into global variables.
- **django/seasight_forecasting/GenerateKML.py**: This file contains the methods to create the KML file.
- **django/seasight_forecasting/global_vars.py**: This file contains a list of global variable that are filled with information from configuration file.
- **django/seasight_forecasting/ManageData.py**: This file contains the methods related to data management: filtering, data loading, data from API downloading, ...
- **django/seasight_forecasting/ManageModel.py**: This file contains the methods related to Deep Learning model management: model loading, data prediction, ...
- **django/seasight_forecasting/tests.py**: This file contains the list of the application tests.

### Configuration File
```bash
[FILES]
historic_data_path = ../data/
historic_data_file = historic.csv
prediction_model_path = ../model/
prediction_model_file = lr_model.pkl
regions_path = ../data/regions/
north_atlantic_region_file = north_atlantic.geojson
south_atlantic_region_file = south_atlantic.geojson
indian_region_file = indian.geojson
west_pacific_region_file = west_pacific.geojson
east_pacific_region_file = east_pacific.geojson
kml_destination_path = seasight_forecasting/static/seasight_forecasting/kml/
kml_destination_file = SST_regions.kml
image_destination_path = seasight_forecasting/static/seasight_forecasting/img/

[KML]
number_of_clusters = 400
cmap = PRGn
```

- **[FILES] section**: This section includes all paths and file names of non-application data.
- **[KML] section**: This section includes the necessary parameters for the KML creation, such as the number of clusters to display and the colormap for the regions color.

## Installing / Getting started
[Install Guide](../master/docs/INSTALL.md)

### Built With
Python3, Django

## Licensing
[MIT License](../master/LICENSE) - Copyright (c) 2020 Gabriel Izquierdo Alcaraz