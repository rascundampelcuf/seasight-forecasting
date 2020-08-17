
import itertools
import os
#import simplekml
from seasight_forecasting import global_vars
from threading import Thread
from time import sleep, time

def sendKmlToLG(main, slave):
    command = "sshpass -p " + global_vars.lg_pass + " scp $HOME/" + global_vars.project_location \
        + "Seasight-Forecasting/django/" + global_vars.kml_destination_path + main \
        + " " + global_vars.lg_IP + ":/var/www/html/SF/" + global_vars.kml_destination_filename
    print(command)
    os.system(command)
    command = "sshpass -p " + global_vars.lg_pass + " scp $HOME/" + global_vars.project_location \
        + "Seasight-Forecasting/django/" + global_vars.kml_destination_path + slave + " " \
        + global_vars.lg_IP + ":/var/www/html/kml/slave_" + str(global_vars.screen_for_colorbar) + ".kml"
    print(command)
    os.system(command)
    command = "sshpass -p " + global_vars.lg_pass + " ssh " + global_vars.lg_IP \
        + " \"echo http://" + global_vars.lg_IP + ":81/SF/" + global_vars.kml_destination_filename + "?id=" + str(int(time()*100)) \
        + " > /var/www/html/kmls.txt\""
    print(command)
    os.system(command)

def sendKmlToLGCommon(filename):
    sendKmlToLG(filename, filename)

def sendKmlToLGHistoric(files):
    sendKmlToLG(files[0], files[1])

def threaded_function():
    files = os.listdir(global_vars.kml_destination_path)
    files = [i for i in files if i.startswith('historic')]
    writeVerbose(str(files))
    main = []
    slave = []
    for elem in files:
        if elem.endswith('slave_{}.kml'.format(global_vars.screen_for_colorbar)):
            slave.append(elem)
        else:
            main.append(elem)
    writeVerbose('main: ' + str(main))
    writeVerbose('slave: ' + str(slave))
    for elem in itertools.cycle(list(zip(main, slave))):
        sendKmlToLG(elem)
        sleep(global_vars.sleep_in_thread)
        if global_vars.thread == False:
            print("thread finished...exiting")
            break

def startSendKMLThread():
    global_vars.thread = True
    thread = Thread(target = threaded_function)
    thread.name = 'SendKML'
    thread.start()

def stopSendKMLThread():
    global_vars.thread = False

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

def doRotation(playList, latitude, longitude, altitude, pRange):
    for angle in range(0, 360, 10):
        flyto = playList.newgxflyto(gxduration=1.0)
        #flyto.gxflytomode = simplekml.GxFlyToMode.smooth
        #flyto.altitudemode = simplekml.AltitudeMode.relativetoground

        #flyto.lookat.gxaltitudemode = simplekml.GxAltitudeMode.relativetoseafloor
        flyto.lookat.longitude = float(longitude)
        flyto.lookat.latitude = float(latitude)
        flyto.lookat.altitude = altitude
        flyto.lookat.heading = angle
        flyto.lookat.tilt = 77
        flyto.lookat.range = pRange

def cleanVerbose():
    fName = 'seasight_forecasting/static/scripts/verbose.txt'
    with open(fName, "w"):
        pass

def writeVerbose(text):
    fName = 'seasight_forecasting/static/scripts/verbose.txt'
    with open(fName, "a+") as f:
        f.seek(0)
        data = f.read()
        if len(data) > 0 :
            f.write("<br>")
        f.write(text)

def getCenterOfRegion(region):
    lon = region.centroid.coords.xy[0][0]
    lat = region.centroid.coords.xy[1][0]
    return lat, lon

def flyToRegion(region):
    center_lat, center_lon = getCenterOfRegion(region)
    sendFlyToToLG(center_lat, center_lon, 15000000, 0, 0, 15000000, 2)

def logprint(text):
    if global_vars.logs:
        print(text)