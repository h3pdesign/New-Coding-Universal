function Get-FolderSize {
param ( [Parameter(Mandatory=$true)] [System.String]${Path} )
 
$objFSO = New-Object -com  Scripting.FileSystemObject
$folders = (dir $path | ? {$_.PSIsContainer -eq $True})
foreach ($folder in $folders)
    {
    $folder | Add-Member -MemberType NoteProperty -Name "SizeMB" -Value (($objFSO.GetFolder($folder.FullName).Size) / 1MB) -PassThru
    }
 
}
Get-FolderSize $args[0]

#$folders = icm $allServers -FilePath C:\Scripts\Get-FolderSize.ps1 -ArgumentList "E:\Profiles"
#$folders | sort -Property SizeMB -Descending | select fullname,@{n='SizeMBN2';e={"{0:N2}" -f $_.SizeMB}} | select -First 10