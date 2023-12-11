
Get-WmiObject win32_networkadapterconfiguration -filter "ipenabled = 'True'" -ComputerName $computername |
Select PSComputername,
@{Name = "IPAddress";Expression = {
[regex]$rx = "(\d{1,3}(\.?)){4}"
$rx.matches($_.IPAddress).Value}},MACAddress