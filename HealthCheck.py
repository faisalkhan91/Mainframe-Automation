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

    #