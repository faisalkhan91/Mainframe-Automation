import time
import yaml


# Method to write metric logs to file
def metric_log(code):
    # Reading configuration file (Check config/config.yml)
    with open("config/config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    
    current_time = time.strftime("%m/%d/%y %H:%M %p", time.localtime())
    # File name and location
    filename = cfg["logs"]["metric"] + cfg["files"]["metric_filename"] + '.txt'
    # Write logs to file
    with open(filename, 'w') as file:
        if code == 'x00':
            msg = current_time + ' Mainframe Application Health Check: PASS'
        else:
            msg = current_time + ' Mainframe Application Health Check: FAIL'
        file.write(msg)