#!/usr/bin/env python
# -*- coding: utf-8 -*-

from py3270 import Emulator

# Function Definitions
from modules.MetricLog import *
from modules.DetailLog import *
from modules.ExecutionLog import *
from modules.LogCopy import *


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
    
    # raise ValueError("A very specific bad thing happened.")  # to raise exception for testing.
        
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
    step_desc = "Launch SRO Application"
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