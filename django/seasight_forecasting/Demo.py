
import os
from seasight_forecasting import global_vars
from time import sleep, time

def sendKmlToLG(main, slave):
    command = "sshpass -p " + global_vars.lg_pass + " scp $HOME/" + global_vars.project_location \
        + "Seasight-Forecasting/django/" + main + " " + global_vars.lg_IP + ":/var/www/html/SF/" + global_vars.kml_destination_filename
    print(command)
    os.system(command)

    command = "sshpass -p " + global_vars.lg_pass + " ssh " + global_vars.lg_IP \
        + " \"echo "  \
        + " > /var/www/html/kml/slave_" + str(global_vars.screen_for_colorbar) + ".kml\""
    print(command)
    os.system(command)
    command = "sshpass -p " + global_vars.lg_pass + " scp $HOME/" + global_vars.project_location \
        + "Seasight-Forecasting/django/" + slave + " " \
        + global_vars.lg_IP + ":/var/www/html/kml/slave_" + str(global_vars.screen_for_colorbar) + ".kml"
    print(command)
    os.system(command)

    command = "sshpass -p " + global_vars.lg_pass + " ssh " + global_vars.lg_IP \
        + " \"echo http://" + global_vars.lg_IP + ":81/SF/" + global_vars.kml_destination_filename + "?id=" + str(int(time()*100)) \
        + " > /var/www/html/kmls.txt\""
    print(command)
    os.system(command)

def LoadKML(path):
    sendKmlToLG(path + 'SST_regions.kml', path + 'slave.kml')

def FlyTo(position):
    pass

def SouthAtlantic():
    LoadKML(global_vars.demo_files_path + 'South_Atlantic/')

def Indian():
    LoadKML(global_vars.demo_files_path + 'Indian/')

def WestPacific():
    LoadKML(global_vars.demo_files_path + 'West_Pacific/')

def EastPacific():
    LoadKML(global_vars.demo_files_path + 'East_Pacific/')

def NorthAtlantic():
    LoadKML(global_vars.demo_files_path + 'North_Atlantic/')

def GenerateDemo():
    SouthAtlantic()
    Indian()
    WestPacific()
    EastPacific()
    NorthAtlantic()