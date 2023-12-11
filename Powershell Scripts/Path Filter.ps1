
#Parameters

$SourcePath = "\\?\C:\Temp\" 	## --- Put Folder-Path Here 
$outputFilePath = "C:\Test Output Skript\PathLengths.txt" # This must be a file in a directory that exists and does not require admin rights to write to.

#Get directory list, silently continue on errors in case script isn't run as an admin and there are system folders
$folders =  Get-ChildItem -Path $SourcePath -Recurse -Depth 3 -Exclude *System* -ErrorAction SilentlyContinue | 
    Select-Object -Property FullName, @{Name="FullNameLength";Expression={($_.FullName.Length -gt 259)}}|
    Sort-Object -Property FullName -Descending | 
    ForEach-Object {
                    $filePath = $_.FullName
                    $length = $_.FullNameLength
                    $string = "$length : $filePath"
                    #Export-Csv $string -Path $outputFilePath -NoTypeInformation -append
                    }
#Loop through folders, checking each for files
$files = For ($i = 0; $i -lt $folders.count; $i++) {
    #Update progress bar for current folder
    Write-Progress -Activity "Collecting Folders paths..." -CurrentOperation "Collecting Folders path length..." -PercentComplete (($i + 1) / $folders.count * 100) -Status ("Folder {0} of {1}" -f ($i + 1), $folders.count)
    Get-ChildItem $folders[$i].FullName -ea 4
}

$folders |
    Select-Object -Property Name, Created, LastWrite, Size, FullNameLength |
    Export-Csv -Path $outputFilePath -NoTypeInformation