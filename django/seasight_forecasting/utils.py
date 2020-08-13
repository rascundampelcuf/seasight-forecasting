
import os
from seasight_forecasting import global_vars

def sendKmlToLG():
    command = "sshpass -p " + global_vars.master_pass +" scp $HOME/" + global_vars.project_location \
        + "Seasight-Forecasting/django/" + global_vars.kml_destination_path + global_vars.kml_destination_filename \
        + global_vars.master_IP + ":/var/www/html/" + global_vars.kml_destination_filename
    os.system(command)
