# File to save the logs
Start-Transcript -Path "PSScriptRoot\..logs\Execution\Script_Transcript_$(get-date -f MMddyyyy_HHmmss_tt).txt"

ScriptRoot\.."
-v "$PSScriptRoot\..\HealthCheck.py"

anscript

leep -Seconds 5
