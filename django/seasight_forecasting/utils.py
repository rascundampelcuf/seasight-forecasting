
import itertools
import os
from seasight_forecasting import global_vars
from threading import Thread
from time import sleep, time

def sendKmlToLG(filename):
    command = "sshpass -p " + global_vars.lg_pass + " scp $HOME/" + global_vars.project_location \
        + "Seasight-Forecasting/django/" + global_vars.kml_destination_path + filename \
        + " " + global_vars.lg_IP + ":/var/www/html/SF/" + global_vars.kml_destination_filename
    print(command)
    command = "sshpass -p " + global_vars.lg_pass + " scp $HOME/" + global_vars.project_location \
        + "Seasight-Forecasting/django/" + global_vars.kml_destination_path + "slave_" + global_vars.screen_for_colorbar \
        + ".kml " + global_vars.lg_IP + ":/var/www/html/kml/slave_" + global_vars.screen_for_colorbar + ".kml"
    print(command)
    os.system(command)
    os.system(command)
    command = "sshpass -p " + global_vars.lg_pass + " ssh " + global_vars.lg_IP \
        + " \"echo http://localhost:81/SF/" + global_vars.kml_destination_filename + "?id=" + str(int(time()*100)) \
        + " > /var/www/html/kmls.txt\""
    print(command)
    os.system(command)

def threaded_function():
    files = os.listdir(global_vars.kml_destination_path)
    files = [i for i in files if i.startswith('historic')]
    for elem in itertools.cycle(files):
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