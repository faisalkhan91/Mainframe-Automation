import os
import sys
import subprocess


# Copy files to shared drive
def copy_logs():
    clone_log_path = os.path.abspath("var\\CloneLogs.ps1")
    clear_files_path = os.path.abspath("var\\ClearFiles.ps1")
    p = subprocess.Popen(["powershell.exe",
                          str(clone_log_path)],
                         stdout=sys.stdout)
    p.communicate()
    p = subprocess.Popen(["powershell.exe",
                          str(clear_files_path)],
                         stdout=sys.stdout)
    p.communicate()
    