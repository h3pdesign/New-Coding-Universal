#Important Cmdlets

Get-CimInstance -ClassName Win32_ComputerSystem -ComputerName . | Select-Object -Property SystemType

Get-CimInstance -ClassName Win32_ComputerSystem

Get-CimInstance -ClassName Win32_LogicalDisk -Filter "DriveType=3" -ComputerName 

# One line script to return current IPv4 addresses on a Windows host
Get-NetIPAddress | Where-Object { $_.AddressFamily -eq 'IPv4' } | ForEach-Object IPAddress