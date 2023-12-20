## -- Parameters

$SourcePath = "C:\" 	## --- Put Folder-Path Here  = foreach($server in (Get-Content "C:\Servers.txt")){
#$SourcePath = "\\?\C:\Temp\" 
$outputFilePath = "C:\Test Output Skript\PathLengths.txt" # This must be a file in a directory that exists and does not require admin rights to write to.
#$ImportPath = 
$writeToConsoleAsWell = $false   # Writing to the console will be much slower.
$Excludes = @("PerfLogs", "boot", "MSOCache", "programdata", "Windows", "System Volume Information", '\$Recycle\.Bin')
#$regex = "($($Exclude -join "|"))"

## -- Begin-block

    #$Result = Get-ChildItem -Path $SourcePath -File -Recurse -Force | 
    #Select FullName, @{Name="Path";Expression={$_.FullName.length -gt 250}}

    ## -- Open a new file stream (nice and fast) and write all the paths and their lengths to it.
	$outputFileDirectory = Split-Path $outputFilePath -Parent
    #Convert-Path $SourcePath | % {
    #If (Test-Path $_) { 
    if (!(Test-Path $outputFileDirectory)) { New-Item $outputFileDirectory -ItemType Directory }
    $stream = New-Object System.IO.StreamWriter($outputFilePath, $true)

    ## -- Execute The PowerShell Code and Update the Status of the Progress-Bar
	#Working: 
	#Result = Get-ChildItem -Path $SourcePath -Recurse -Force -Depth 3 | 
	$Result = Get-ChildItem -Path $SourcePath -Recurse -Depth 3 -Exclude *System* -ErrorAction SilentlyContinue | 
	#? { $_.fullname -notmatch $regex } | -Force
    #? { $_.PsIsContainer -and $_.FullName -notmatch $Excludes } |
    #Out-GridView -PassThru |
    S elect-Object -Property FullName, 
                @{Name = "FullNameLength"; Expression = { ($_.FullName.Length -gt 259) } } |
    Where-Object -FilterScript {$_.FullName -contains "true"} |
    Sort-Object -Property FullName -Descending | 						
    ForEach-Object {
        $filePath = $_.FullName
        $length = $_.FullNameLength
        $string = "$length : $filePath"

        ## -- Write to the Console.
        if ($writeToConsoleAsWell) { Write-Host $string }
        ##Write to the file.
        $stream.WriteLine($string)    
    }
    $stream.Close()

