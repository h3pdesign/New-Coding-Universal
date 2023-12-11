## -- Parameters

$SourcePath = "\\?\C:\" 	## --- Put Folder-Path Here  = foreach($server in (Get-Content "C:\Servers.txt")){
#$SourcePath = "\\?\C:\Temp\" 
$outputFilePath = "C:\Test Output Skript\PathLengths.txt"

$Folders = Get-ChildItem $SourcePath |
    Where-Object { $_.PSIsContainer -eq $true } |
    Sort-Object

$Results = foreach( $Folder in $Folders ){ 
    $FolderSize = Get-ChildItem $Folder.FullName -Recurse -Force |
        Where-Object { $_.PSIsContainer -eq $false } |
        Measure-Object -Property Length -Sum |
        Select-Object -ExpandProperty Sum

    $Properties = @{
        Name = "FullNameLength"; Expression = { ($_.FullName.Length -gt 259) } 
        #Name = $Folder.Name -gt 259
        Created = $Folder.CreationTime
        LastWrite = $Folder.LastWriteTime
        Size = "$( $FolderSize / 1MB ) MB"
        
        }

    New-Object -TypeName PSCustomObject -Property $Properties
    }

$Results |
    Select-Object -Property Name, Created, LastWrite, Size, FullNameLength |
    Export-Csv -Path $outputFilePath -NoTypeInformation -append