# Libraries imported
from datetime import datetime, date
import yaml


def build_time(time_string):
    return datetime.combine(date.today(), datetime.strptime(time_string, "%m/%d/%y %H:%M:%S %p").time())


# Method to write detail logs to the log file.
def detail_log(timestr, step_num, step_desc, start, end, code):
    # Reading configuration file (Check config/config.yml)
    with open("config/config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    
    # Filename and location
    filename = cfg["logs"]["detail"] + cfg["files"]["detail_filename"] + timestr + '.txt'

    # Log Parameters
    app_name = cfg["detail"]["app_name"]
    step = 'STEP'
    step_number = str(step_num)
    step_description = step_desc
    description = ''
    start_time = start
    end_time = end
    duration = build_time(end_time) - build_time(start_time)
    status = ''

    if code == 'x00':
        status = 'PASS'
    elif code == 'x01':
        status = 'FAIL'
    elif code == 'x02':
        step = 'SUMMARY'
        step_number = 'n/a'
        step_description = 'n/a'
        status = 'PASS'
    elif code == 'x03':
        step = 'SUMMARY'
        step_number = 'n/a'
        step_description = 'n/a'
        status = 'FAIL'
    
    # Write logs to file
    with open(filename, 'a') as file:
        print_log = app_name + ',' + step + ',' + step_number + ',' + step_description + ',' + description + ',' \
                    + str(start_time) + ',' + str(end_time) + ',' + str(duration) + ',' + status
        
        file.write(print_log)
        file.write('\n')
    
'''
- Below is the standard log format representation.

App name,STEP,1,Generic step description,00/00/2024 00:00:00 AM,00/00/2024 0.00:00:00 AM,PASS
App name,STEP,2,Generic step description,00/00/2024 00:00:00 AM,00/00/2024 0.00:00:00 AM,PASS
App name,STEP,3,Generic step description,00/00/2024 00:00:00 AM,00/00/2024 0.00:00:00 AM,PASS
App name,STEP,4,Generic step description,00/00/2024 00:00:00 AM,00/00/2024 0.00:00:00 AM,PASS
App name,SUMMARY,n/a,n/a,00/00/2024 00:00:00 AM,00/00/2024 0.00:00:00 AM,PASS

Generic step description examples to use consistently across the board:

Landing Page
Authorization
Retrieve Content
Login
Logout
Launch such and such
Validate such and such
'''