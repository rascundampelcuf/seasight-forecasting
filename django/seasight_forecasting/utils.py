
import itertools
import os
from seasight_forecasting import global_vars
from threading import Thread
from time import sleep

def sendKmlToLG(filename):
    command = "sshpass -p " + global_vars.master_pass +" scp $HOME/" + global_vars.project_location \
        + "Seasight-Forecasting/django/" + global_vars.kml_destination_path + filename \
        + " " + global_vars.master_IP + ":/var/www/html/SF/" + global_vars.kml_destination_filename
    print(command)
    os.system(command)

def threaded_function():
    files = os.listdir(global_vars.kml_destination_path)
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