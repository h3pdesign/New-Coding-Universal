set-executionpolicy remotesigned
#Get-DfsnRoot -Path "\\gll\gll-abl" | Format-List

function  Compare-DFStoFolders{

<#$Servers = @("GLL-AUR-FS61",
"GLL-EMD-FS61",
"GLL-LER-FS61",
"GLL-NOR-FS61",
"GLL-WTM-FS61",
"GLL-VAR-FS61",
"GLL-WHV-FS61",
"GLL-BS-FS61",
"GLL-WOB-FS61",
"GLL-SZ-FS61",
"GLL-WF-FS61",
"GLL-PE-FS61",
"GLL-HE-FS61",
"GLL-CE-FS61",
"GLL-GF-FS61",
"GLL-HM-FS61",
"GLL-H2-FS61",
"GLL-H4-FS61",
"GLL-RI-FS61",
"GLL-ALF-FS61",
"GLL-HI-FS61",
"GLL-LG-FS61",
"GLL-UE-FS61",
"GLL-LUE-FS61",
"GLL-WL-FS61",
"GLL-NOM-FS61",
"GLL-GOE-FS61",
"GLL-OHA-FS61",
"GLL-HOL-FS61",
"GLL-GS-FS61",
"GLL-CLP-FS61",
"GLL-OL-FS61",
"GLL-WST-FS61",
"GLL-BRA-FS61",
"GLL-DEL-FS61",
"GLL-WDH-FS61",
"GLL-VEC-FS61",
"GLL-OS-FS61",
"GLL-MEP-FS61",
"GLL-LIN-FS61",
"GLL-PAP-FS61",
"GLL-NOH-FS61",
"GLL-OTT-FS61",
"GLL-OHZ-FS61",
"GLL-STD-FS61",
"GLL-BHV-FS61",
"GLL-BRV-FS61",
"GLL-ROW-FS61",
"GLL-SUL-FS61",
"GLL-VER-FS61",
"GLL-NI-FS61",
"GLL-SY-FS61",
"GLL-FAL-FS61")#>


$Servers = @("GLL-AUR-FS61","GLL-EMD-FS61","GLL-LER-FS61")

$FolderPaths = $Servers | foreach {
    Get-ChildItem "\\$_\DFSShare$"
} | Sort Path

$FolderPaths | Export-Csv "FolderPaths-$(Get-Date -format yyyy-MM-dd).csv" -NoTypeInformation

$TestPaths = (($FolderPaths).FullName | Sort-Object).Trimend('\')
$DFSPaths = ((Import-CSV "DFS-$(Get-Date -format yyyy-MM-dd).csv").TargetPath | Where-Object {($_ -ilike "*SERVER*") | Sort-Object).Trimend('\')

$TestPaths | Where-Object {$DFSPaths -notcontains $_}
}