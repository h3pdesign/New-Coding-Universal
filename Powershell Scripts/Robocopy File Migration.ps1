robocopy "<source replicated folder path>" "<destination replicated folder path>" /e /b /copyall /r:6 /w:5 /MT:64 /xd DfsrPrivate /tee /log:<log file path> /v1robocopy "<source replicated folder path>" "<destination replicated folder path>" /e /b /copyall /r:6 /w:5 /MT:64 /xd DfsrPrivate /tee /log:<log file path> /v

robocopy.exe "\\SERVER01\e$\RF01" "d:\RF01" /e /b /copyall /r:6 /w:5 /MT:64 /xd DfsrPrivate /tee /log:c:\temp\preseed-server02.log

# Step 1
robocopy \\OLDSERVER\d$\FOLDER D:\FOLDER /e /zb /copy:DATSOU /r:3 /w:3 /log:c:\ROBOCOPY-Logs\FOLDER.log /V /NP


# Step 2
robocopy \\OLDSERVER\d$\FOLDER D:\FOLDER /e /zb /copy:DATSOU /MIR /r:3 /w:3 /log:c:\ROBOCOPY-Logs\Last-Copy\FOLDER.log /V /NP


#Script

# Uses relative paths
# Make sure you change directory to where your script is located on the computer you are running this before running
#
# =========================================================================================
#Function: Get the Total Size of Folder
function Get-Size {
    param([string]$pth)
    “{0:n2}” -f ((gci -path $pth -recurse | measure-object -property length -sum).sum / 1mb) + ” mb”
}
# =========================================================================================
#
cd “C:\PSScripts\OldServerName”
$SourceServerNetBIOSName = “OldServerName”
$SourceServerIP = “10.100.200.200”
$DestinationServerName = “NewFileServer.contoso.com”
#**************************************************************************************
#Ignore this section
#Test files with only one share
#Note: This section was a test to see if I can get this script to work if there is only one share.
#I could not get it to work with one share. The reason is there must be two (2) or more shares for
#this to work, because I’m using an array. There is no such thing as a single array.
#$SourceServerPath =            @()
#$SourceServerShares =          @()
#$DestinationServerShareNames = @()
#$SourceServerPath =            Get-Content ‘.\OldServerName-Share-paths-test.txt’
#$SourceServerShares =          Get-Content ‘.\OldServerName-SourceSharesList-test.txt’
#$DestinationServerShareNames = Get-Content ‘.\OldServerName-DestinationSharesList-test.txt’
#Ignore this section
#**************************************************************************************
$SourceServerPath = Get-Content ‘.\OldServerName-Share-paths.txt’
$SourceServerShares = Get-Content ‘.\OldServerName-SourceSharesList.txt’
$DestinationServerShareNames = Get-Content ‘.\OldServerName-DestinationSharesList.txt’
$LogDestinationFolder = “.\Logs” 
$LogfileName = $SourceServerNetBIOSName + ”.txt”
$LogFileAndPath = $LogDestinationFolder + ”\” + $LogfileName
# Checks for existence of a directory for log files if not, one gets created.
If (!(Test-Path -Path $LogDestinationFolder)) {
    New-Item -ItemType directory -Path $LogDestinationFolder
}
write-host “Total Share count = ” $SourceServerShares.count
for ($i = 0; $i -lt $SourceServerShares.count; $i++) {
    $srcpath = $SourceServerPath[$i] -replace ‘(.*):’, ’$1$’
    #$srcpath = $SourceServerPath -replace ‘(.*):’,’$1$’
    $dstpath = $DestinationServerShareNames[$i]
    $FullSourcePath = “\\” + $SourceServerIP + ”\” + $srcpath
    $FullDestPath = “\\” + $DestinationServerName + ”\” + $dstpath
    write-host “”
    
    if ((Test-Path $FullSourcePath) -and (Test-Path $FullDestPath)) {
        $log = $LogDestinationFolder + “\” + $SourceServerNetBIOSName + “-” + $SourceServerShares[$i] + ”.txt”
        write-host “Current share’s log:” $Log
        
        robocopy $FullSourcePath $FullDestPath /E /R:1 /W:1 /TEE /log:$log | Out-String
        #This is trying different switches – Ignore
        #robocopy $FullSourcePath $FullDestPath /MIR /copy:DT /W:5 /R:1 /V /IT /FP /NFL /TS  /log:$log | Out-String
        #This was a local drive to drive attempt – Ignore
        #robocopy e:\users y: /copy:DATSO /E /R:1 /W5 /TEE /log:c:\robocopy.log 
        write-host “Source path is: ” $srcpath 
        write-host “Full Source Path is: ” $FullSourcePath
        write-host “Destination path is:” $dstpath
        write-host “Full Destination path is: ” $FullDestPath
        $SharesProcessedSoFar = $i + 1
        write-host “Shares processed so far =” $SharesProcessedSoFar ” out of a total share count of ” $SourceServerShares.count
        write-host “”
        Write-Host “”
    } 
    else {
        write-host “Problem with: ”           $srcpath         “Destination sharename is:”     $dstpath
        write-host “Referencing full Source Path:” $FullSourcePath  “Destination Path:”         $FullDestPath
        $SharesProcessedSoFar = $i + 1
        write-host “Shares processed so far =” $SharesProcessedSoFar ” out of a total share count of ” $SourceServerShares.count
    }
}
write-host “Total Shares processed = ” $SourceServerShares.count