# File to save the logs.
Start-Transcript -Path "PSScriptRoot\..logs\Execution\Script_Transcript_$(get-date -f MMddyyyy_HHmmss_tt).txt"

cd "$PSScriptRoot\.."
python -v "$PSScriptRoot\..\HealthCheck.py"

Stop-Transcript

Start-Sleep -Seconds 5
