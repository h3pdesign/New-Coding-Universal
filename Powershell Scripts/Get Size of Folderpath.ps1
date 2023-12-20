# Function: Get the Total Size of Folder
function Get-Size {
    param([string]$pth)
    “{0:n2}” -f ((gci -path $pth -recurse | measure-object -property length -sum).sum / 1mb) + ” mb”
}

# First
# Command for path length greater than 260 characters 
#Get-ChildItem | Get-FolderItem
#Get-FolderItem -Path .\PowerShellScripts

cmd /c dir "\\?\C:\" /s /b /a | ? { $_.length -gt 260 } | Out-File C:\Users\hipeders\list.txt -width 300

Get-ChildItem \\?\C:\Users\hipeders\ -Recurse -Force -ErrorAction SilentlyContinue | 
  Where-Object {$_.FullName.Length -gt 255}
    Export-Csv "C:\Users\hipeders\Test\Results.csv" -NoTypeInformation -append 

#or

$files = Get-ChildItem '\\?\C:\Users\Documents\' -recurse | where { $_.fullname.length -gt 250 } | select -ExpandProperty fullname
$files | export-csv 'Results.csv' -noclobber

#or 

Get-ChildItem -r * |? {$_.GetType().Name -match "File" } |? {$_.fullname.length -ge 260} |%{$_.fullname} > C:\Export_FileDepth.txt


# Second FullName.length -gt 255 
Get-ChildItem -Path C:\Users\hipeders\Test -Recurse |`
    foreach {
    $Item = $_
    $Type = $_.Extension
    $Path = $_.FullName
    $Folder = $_.PSIsContainer
    $Age = $_.CreationTime

    $Path | Select-Object `
    @{n = "Name"; e = { $Item } }, `
    @{n = "Created"; e = { $Age } }, `
    @{n = "filePath"; e = { $Path } }, `
    @{n = "Extension"; e = { if ($Folder) { "Folder" }else { $Type } } }`
} | Export-Csv "C:\Users\hipeders\Test\Results.csv" -NoTypeInformation -append 

#Third robocopy
$item = "PowerShellScripts"
$params = New-Object System.Collections.Arraylist
$params.AddRange(@("/L", "/S", "/NJH", "/BYTES", "/FP", "/NC", "/NDL", "/TS", "/XJ", "/R:0", "/W:0"))
$countPattern = "^\s{3}Files\s:\s+(?<Count>\d+).*"
$sizePattern = "^\s{3}Bytes\s:\s+(?<Size>\d+(?:\.?\d+)\s[a-z]?).*"
$files = Get-FolderItem -Path .\PowerShellScripts
$files | Measure-Object -Sum -Property Length | 
((robocopy $item NULL $params)) | ForEach {
    If ($_ -match "(?<Size>\d+)\s(?<Date>\S+\s\S+)\s+(?<FullName>.*)") {
        New-Object PSObject -Property @{
            FullName = $matches.FullName
            Size     = $matches.Size
            Date     = [datetime]$matches.Date
        }
    }
    Else {
        Write-Verbose ("{0}" -f $_)
    }
}

