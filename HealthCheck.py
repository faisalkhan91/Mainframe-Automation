#!/usr/bin/env python
# -*- coding: utf-8 -*-

from py3270 import Emulator

# Function Definitions
from modules.MetricLog import *
from modules.DetailLog import *
from modules.ExecutionLog import *
from modules.LogCopy import *
#from modules.Retry import *


def get_time():
    return datetime.now().strftime("%m/%d/%y %H:%M:%S %p")
    # return time.strftime("%m/%d/%y %H:%M:%S %p", time.localtime())  # Using time

def set_mode(cfg):
    if cfg["default"]["mode"] == 'Normal':
        return 0
    elif cfg["default"]["mode"] == 'Slow':
        return 2

def main():
    # Read config file
    with open("config/config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    
    # raise ValueError('A very specific bad thing happened.')  # To raise exception for testing.
        
    # Initial Declaration
    timestr = time.strftime("%Y%m%d_%H%M%S_%p")
    start_execution = get_time()
    code = 'x00'
    wait_time = cfg["default"]["wait"]
    slow_mode = set_mode(cfg)

    em = Emulator(visible=True, args=["-model", "2"])  # This uses x3270, so you can see what is going on.

    # Detail log parameters
    detail_log_list = []

    # Connection Sequence
    step_num = 1
    step_desc = "Launch Application"
    start = get_time()
    em.connect(cfg["default"]["host"])
    # detail_log(timestr, step_num, step_desc, start, end=get_time(), code='x00')
    detail_log_list.append([timestr, step_num, step_desc, start, get_time(), 'x00'])

    # Login
    step_num = 2
    step_desc = "Login"
    start = get_time()
    em.fill_field(24, 25, cfg["default"]["system"], 4)
    em.send_enter()
    time.sleep(wait_time)
    em.fill_field(12, 21, cfg["credentials"]["user"], 4)  # Mainframe Id
    time.sleep(slow_mode)
    em.send_enter()
    em.fill_field(13, 21, cfg["credentials"]["password"], 8)  # Mainframe Password
    time.sleep(slow_mode)
    em.send_enter()
    time.sleep(wait_time)
    # Login Success/Failure
    if em.string_found(5, 30, 'SIGNON OK'):
        print('Login successful.')
        # detail_log(timestr, step_num, step_desc, start, end=get_time(), code='x00')
        detail_log_list.append([timestr, step_num, step_desc, start, get_time(), 'x00'])
    elif not em.string_found(5, 30, 'SIGNON OK'):
        # metric_log(code='x01')
        # detail_log(timestr, step_num, step_desc, start, end=get_time(), code='x01')
        code = 'x01'
        detail_log_list.append([timestr, step_num, step_desc, start, get_time(), 'x01'])
        # if cfg["default"]["copy_logfile"] == 'ON':
        #     copy_logs()
        # else:
        #     pass
        # sys.exit('Error: Script exited. Login not found.')

    # - Perform Operation
    step_num = 3
    step_desc = "Validate system"
    start = get_time()
    em.fill_field(1, 2, '<WHAT TO INPUT>', 8)
    time.sleep(slow_mode)
    em.send_enter()
    time.sleep(wait_time)
    # Application Load Success/Failure
    if em.string_found(1, 34, 'MAIN MENU'):
        print('Application load successful.')
        # detail_log(timestr, step_num, step_desc, start, end=get_time(), code='x00')
        detail_log_list.append([timestr, step_num, step_desc, start, get_time(), 'x00'])
    elif not em.string_found(1, 34, 'MAIN MENU'):
        # metric_log(code='x01')
        # detail_log(timestr, step_num, step_desc, start, end=get_time(), code='x01')
        code = 'x01'
        detail_log_list.append([timestr, step_num, step_desc, start, get_time(), 'x01'])
        # if cfg["default"]["copy_logfile"] == 'ON':
        #     copy_logs()
        # else:
        #     pass
        # sys.exit('Error: Script exited. Login not found.')
    
    # - Logout
        step_num = 4
        step_desc = "Logout"
        start = get_time()
        em.fill_field(21, 13, '<INPUT>', 2)
        time.sleep(slow_mode)
        em.send_enter()
        time.sleep(wait_time)
        # Sign off search
        if em.string_found(24, 1, 'ENTER APPLICATION NAME'):
            print('Logout successful.')
            # detail_log(timestr, step_num, step_desc, start, end=get_time(), code='x00')
            detail_log_list.append([timestr, step_num, step_desc, start, get_time(), 'x00'])
        elif not em.string_found(24, 1, 'ENTER APPLICATION NAME'):
            # metric_log(code='x01')
            # detail_log(timestr, step_num, step_desc, start, end=get_time(), code='x01')
            code = 'x01'
            detail_log_list.append([timestr, step_num, step_desc, start, get_time(), 'x01'])
            # if cfg["default"]["copy_logfile"] == 'ON':
            #     copy_logs()
            # else:
            #     pass
            # sys.exit('Error: Script exited. Sign off error.')

        # - Terminate Application
        # Disconnect from host and kill subprocess
        step_num = 5
        step_desc = "Terminate Connection"
        em.terminate()
        print("Connection Terminated.")

        metric_log(code)
        # detail_log(timestr, step_num, step_desc, start_execution, end=get_time(), code='x02')

        if detail_log_list[1][5] == 'x00':
            detail_log_list.append([timestr, step_num, step_desc, start_execution, get_time(), 'x02'])
        elif detail_log_list[1][5] == 'x01':
            detail_log_list.append([timestr, step_num, step_desc, start_execution, get_time(), 'x03'])

        for dlog in detail_log_list:
            detail_log(dlog[0], dlog[1], dlog[2], dlog[3], dlog[4], dlog[5])
        
        if cfg["default"["execution_log"]] == 'ON':
            execution_log(timestr)
        elif cfg["default"]["execution_log"] == "OFF":
            print('Execution og writing \'OFF')
        
        if cfg["default"["copy_logfile"]] == 'ON':
            print("Log copy feature is ON")
            copy_logs()
        else:
            # pass
            print("Log copy feature is OFF")

    
    # Main Program
    if __name__ == "__main__":
        try:
            main()
        except Exception as e:
            metric_log(code='x01')

            time_string = time.strftime("%Y%m%d_%H%M%S_%p")
            count = 1
            detail_log_list_execption = ["Launch Application",
                                         "Login",
                                         "Validate System",
                                         "Logout"]
            for log in detail_log_list_execption:
                detail_log(time_string, count, log, get_time(), get_time(), 'x01')
                count += 1
            detail_log(time_string, count, "Terminate Connection", get_time(), get_time(), 'x03')

            print(e)
        