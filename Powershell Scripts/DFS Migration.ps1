#add server to DFS
    $ReplicationFolders = @(“Folder1”,“Folder2”,“Folder3”,“Folder4”,“Folder5”)
    Add-DfsrMember -GroupName “Namespace name \\domain.com\namespace” -ComputerName $Using:NewServer
    $OutPartners = Get-DfsrConnection -SourceComputerName $Using:OldServer
    $InPartners = Get-DfsrConnection -DestinationComputerName $Using:OldServer
    foreach($OutPartner in $OutPartners){
    Add-DfsrConnection -GroupName “Namespace name \\domain.com\namespace” -SourceComputerName $Using:NewServer -DestinationComputerName $OutPartner.DestinationComputerName -CreateOneWay
    }
    foreach($InPartner in $InPartners){
    Add-DfsrConnection -GroupName “Namespace name \\domain.com\namespace” -SourceComputerName $InPartner.SourceComputerName -DestinationComputerName $Using:NewServer -CreateOneWay
    }
    foreach($ReplicationFolder in $ReplicationFolders){
    New-DfsnFolderTarget -Path “\\domain.com\$ReplicationFolder” -TargetPath "\\$Using:NewServerFQDN\$ReplicationFolder"
    Write-Log -Level INFO -Message "$Using:NewServer replication folder $ReplicationFolder has been added to the namespace folder $ReplicationFolder" -logfile $Using:logfileloc
    Set-DfsrMembership -GroupName “Namespace name \\domain.com\$ReplicationFolder” -FolderName “$ReplicationFolder” -ComputerName $Using:NewServer -ContentPath “E:\Shared Folders\namespaces\$ReplicationFolder\”
    Write-Log -Level INFO -Message "$Using:NewServer has been added to the DFS-R membership for $ReplicationFolder in the Namespace name \\domain.com\namespace namespace" -logfile $Using:logfileloc}
    Update-DfsrConfigurationFromAD -ComputerName $Using:NewServer