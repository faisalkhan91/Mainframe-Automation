# File to create mount, workaround since powershell does not support login through ID
$net = new-object -ComObject WScript.Network
$net.MapNetworkDrive('H:', "PATH", $false, "USERNAME", "PASSWORD")

# File to save the logs
#Start-Transscript -Path "logs\$(get-date -f MM_dd_yyyy_) tmp.txt"

Get-ChildItem -Path "$PSScriptRoot\..\logs\Detailed" | Copy-Item -Destination "PATH TO COPY" -Recurse
Get-ChildItem -Path "$PSScriptRoot\..\logs\Metric" | Copy-Item -Destination "PATH TO COPY" -Recurse

#Stop-Transcript

Start-Sleep -Seconds 5
$net.RemoveNetworkDrive('H', "$true");
