$Folder = "$PSScriptRoot\..\logs"

# Delete files older than 7 Days
Get-ChildItem $Folder -Recurse -Force -ea 0 |
? {!$_.PsIsContainer -and $_.LastWriteTime -lt (Get-Date).AddDays(-7)} |
ForEach-Object {
    $_ | del -Force
    $_.FullName | Out-File "$PSScriptRoot\..\logs\Clear" -Append
}

<#
# Delete empty folders and subfolders
Get-ChildItem $Folder -Recurse -Force -ea 0 |
? {$_.PsIsContainer -eq $True} |
? {$_.getfiles().count -eq 0} |
ForEach-Object {
    $_ | del -Force
    $_.FullName | Out-File C:\log\deletelog.txt -Append
}
#>
