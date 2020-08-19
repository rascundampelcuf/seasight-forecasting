
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

def sendFlyToToLG(lat, lon, altitude, heading, tilt, pRange, duration):
    flyTo = "flytoview=<LookAt>" \
            + "<longitude>" + str(lon) + "</longitude>" \
            + "<latitude>" + str(lat) + "</latitude>" \
            + "<altitude>" + str(altitude) + "</altitude>" \
            + "<heading>" + str(heading) + "</heading>" \
            + "<tilt>" + str(tilt) + "</tilt>" \
            + "<range>" + str(pRange) + "</range>" \
            + "<altitudeMode>relativeToGround</altitudeMode>" \
            + "<gx:altitudeMode>relativeToGround</gx:altitudeMode>" \
            + "<gx:duration>" + str(duration) + "</gx:duration>" \
            + "</LookAt>"

    command = "echo '" + flyTo + "' | sshpass -p " + global_vars.lg_pass + " ssh " + global_vars.lg_IP + " 'cat - > /tmp/query.txt'"
    print(command)
    os.system(command)

def LoadKML(path):
    sendKmlToLG(path + 'SST_regions.kml', path + 'slave.kml')

def FlyTo(center_lat, center_lon):
    sendFlyToToLG(center_lat, center_lon, 15000, 0, 0, 6000000, 2)

def SouthAtlantic():
    LoadKML(global_vars.demo_files_path + 'South_Atlantic/')
    FlyTo(-44.033173405198575, -18.55412927249652)
    sleep(10)

def Indian():
    LoadKML(global_vars.demo_files_path + 'Indian/')
    FlyTo(-20.55819005127296, 71.46322969298124)
    sleep(10)

def WestPacific():
    LoadKML(global_vars.demo_files_path + 'West_Pacific/')
    FlyTo(-3.6055350414132112, 148.72609606570853)
    sleep(10)

def EastPacific():
    LoadKML(global_vars.demo_files_path + 'East_Pacific/')
    FlyTo(-14.22202896516345, -129.23682168130628)
    sleep(10)

def NorthAtlantic():
    LoadKML(global_vars.demo_files_path + 'North_Atlantic/')
    FlyTo(43.090963600753945, -25.84386342158867)
    sleep(10)

def GenerateDemo():
    SouthAtlantic()
    Indian()
    WestPacific()
    EastPacific()
    NorthAtlantic()