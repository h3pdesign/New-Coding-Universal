function  Get-DFSFolderTargets {

[CmdletBinding()]
param(
$DFSPath = '\gll*'   #'\DFSNamespace*'
)

Write-Progress "Getting all DFS folders for $DFSPath (this can take a very long time)" -PercentComplete -1
$DFSTree = Get-DfsnFolder $DFSPath

$i = 1
$DFSTree | ForEach-Object{
    Write-Progress "Getting DFS Folder Targets for $($_.Path)" -PercentComplete (($i / $DFSTree.Count) *100)
    
    $DFSTargets = @(Get-DfsnFolderTarget $_.Path | Select Path,TargetPath,State)

    foreach ($DFSTarget in $DFSTargets){
        $Result = [ordered]@{
            Path = $DFSTarget.Path
            TargetPath = $DFSTarget.TargetPath
            State = $DFSTarget.State
            "ValidFrom_$Env:ComputerName" = Test-Path $DFSTarget.Path
        }
        New-Object PSObject -Property $Result
    }
    $i++

} | Sort Path | Export-Csv "DFS-$(Get-Date -format yyyy-MM-dd).csv" -NoTypeInformation
}

Get-DfsnFolderTarget \\gll\gll-abl
Path TargetPath State ReferralPriorityClass ReferralPriorityRank

dir /ad /s "\\gll\gll-abl\" > DFS_Structure.txt