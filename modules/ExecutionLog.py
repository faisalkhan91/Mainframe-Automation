# Libraries imported
import time
import yaml


# Script Execution Log
def execution_log(timestr):
    # Reading configuration file (Check config/config.yml)
    with open("config/config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    
    # Clock time
    current_time = time.strftime("%m/%d/%y %H:%M:%S %p", time.localtime())

    # File name and location
    execution_log_file = cfg["logs"]["execution"] + cfg["files"]["execution_filename"] + timestr + '.txt'

    with open(execution_log_file, 'a') as file:
        print_log = 'This script executed at: ' + current_time + '\n'
        file.write(print_log)
