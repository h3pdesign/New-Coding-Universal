## -- Parameters

$SourcePath = "C:\" 	## --- Put Folder-Path Here  = foreach($server in (Get-Content "C:\Servers.txt")){
#$SourcePath = "\\?\C:\Temp\" 
$outputFilePath = "C:\Test Output Skript\PathLengths.txt"

##  -- Process-block
(Test-Path $SourcePath) { 
$outputFileDirectory = Split-Path $outputFilePath -Parent
if (!(Test-Path $outputFileDirectory)) { New-Item $outputFileDirectory -ItemType Directory }

## -- Execute The PowerShell Code and get Out-GridView
$Result = Get-ChildItem -Path $SourcePath -Recurse -Depth 3 | #?{ $_.fullname -notmatch $regex } | -Force
Out-GridView -PassThru |
Select-Object -Property FullName, @{Name = "FullNameLength"; Expression = { ($_.FullName.Length -gt 259) } } | 
Sort-Object -Property PathLength, FullName, FullNameLength -Descending | #LastWriteTime
ForEach-Object {
    $filePath = $_.FullName
    $length = $_.FullNameLength
    $string = "$length : $filePath"                   
  }

}
