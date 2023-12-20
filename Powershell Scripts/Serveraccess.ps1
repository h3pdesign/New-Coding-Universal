# Remote Script execution

$Server = C:\Temp\ServerList.txt

Invoke-Command -ComputerName   gll-h2-fs61  $Server 
                -ScriptBlock { .\Get-Longpaths.ps1 } 
                -credential nds.pedersen


                get-dnsServer -ComputerName 10.255.255.254

               # Get-ClientAccessServer # Exchange Server
               # Get-RDServer  # Remote Desktop
                Get-StorageFileServer  # What does that?
                Get-StorageFileServer