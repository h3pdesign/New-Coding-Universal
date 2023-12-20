#Examples
#Show complete status in GUI
Get-RvDfsrReport -ComputerName fs0.ad.contoso.com, fs1.ad.contoso.com, fs2.ad.contoso.com |
Out-GridView
#Get full DFS-R report for one defined server and for one defined replication group 
#and replicated folder
Get-RvDfsrReport `
    -ComputerName TESTFILESERVER `
    -GroupName 'Test\FileserTest' `
    -FolderName 'Da*' `
    -BacklogCount BothDirections `
    -BacklogCountError 10000 `
    -Remoting CIM -Verbose

<#
Output:
DestinationComputerName : BIGTARGET
SourceComputerName      : FILESERV44
GroupName               : USA\FILESERV44\D
GroupGuid               : AAAAACCC-4444-5555-1100-1111100000AA
GroupDn                 : CN=USA\FILESERV44\D,CN=DFSR-GlobalSettings,CN=System,                                 DC=contoso,DC=com
GroupIsClustered        : False
GroupScheduleInUtc      : True
FolderGuid              : 99999999-1111-2222-0011-2222266CCCCC
FolderName              : Data
FolderRootPath          : X:\FILESERV44\Data
FolderEnabled           : True
FolderReadOnly          : True
FolderConflictSizeInMB  : 4096
FolderStagingSizeInMB   : 8192
FolderFileFilter        : ~*, *.bak, *.tmp
FolderState             : Initial Sync
BacklogCount            : 286917
BacklogReverseCount     : 53603
BacklogCountSummary     : 340520
ReplicationStatus       : False
Status                  : True
Error                   : False
ErrorDescription        :
#>

#Get DFS-R groups, folders and connections in a second (skip backlog calculations) #for the local server and export it to CSV

Get-RvDfsrReport -BacklogCount Skip -Remoting CIM | Export-Csv `
    -Path 'C:\Temp\My report.csv' `
    -Delimiter "`t" `
    -Encoding UTF8 `
    -NoTypeInformation

    #Display DFS-R report for multiple servers in a console

    Get-RvDfsrReport -ComputerName fs0.ad.contoso.com, fs1.ad.contoso.com, fs2.ad.contoso.com | Format-Table -Property GroupName, FolderName, FolderState, BacklogCount, Status

    #Code
Function Get-RvDfsrReport {
    <#
    .SYNOPSIS
        Get DFS-R status, health and backlogs. Cmdlet (advanced function) is designed to never stop even when it hit an error so the cmdlet will always produce full report with logged errors.

        Description
            Get DFS-R status, health and backlogs. Cmdlet (advanced function) is designed to never stop even when it hit an error so the cmdlet will always produce full report with logged errors.

        Requirements
            Developed and tested using PowerShell 4.0.

    .PARAMETER ComputerName
        Name of the remote server to get report.

        If not set then all groups are queried

    .PARAMETER GroupName
        Name of the group to get report. It is possible to use wildcards (for example MyGroup*).

        If not set then all groups will be queried.

    .PARAMETER FolderName
        Name of the group to get report. It is possible to use wildcards (for example MyGroup*).

        If not set then all folders will be queried.

    .PARAMETER BacklogCount
        Possibilities
            Skip
                Fastest method of generating report.

            Get
                Backlogs are calculated for every folder.

            BothDirections
                Backlogs are calculated for every folder in both directorions.

    .PARAMETER BacklogCountError
        Maximum number of backlogs that is evaluated as normal state.

    .PARAMETER Remoting
        Possibilities
            WMI
                Old method using Get-WmiObject that is compatible with PowerShell 2.0 on Windows Server 2012 R2.

            CIM
                More efficient method using Get-CimInstance that is compatible with PowerShell 3.0 on Windows Server 2012 RTM and with later versions.

    .EXAMPLE
        'Get full DFS-R report for one defined server and for one defined replication group and replicated folder'
        Get-RvDfsrReport `
            -ComputerName BIGTARGET `
            -GroupName 'USA\FILESERV44*' `
            -FolderName 'Da*' `
            -BacklogCount BothDirections `
            -BacklogCountError 10000 `
            -Remoting CIM -Verbose

        Output:
        DestinationComputerName : BIGTARGET
        SourceComputerName      : FILESERV44
        GroupName               : USA\FILESERV44\D
        GroupGuid               : AAAAACCC-4444-5555-1100-1111100000AA
        GroupDn                 : CN=USA\FILESERV44\D,CN=DFSR-GlobalSettings,CN=System,DC=contoso,DC=com
        GroupIsClustered        : False
        GroupScheduleInUtc      : True
        FolderGuid              : 99999999-1111-2222-0011-2222266CCCCC
        FolderName              : Data
        FolderRootPath          : X:\FILESERV44\Data
        FolderEnabled           : True
        FolderReadOnly          : True
        FolderConflictSizeInMB  : 4096
        FolderStagingSizeInMB   : 8192
        FolderFileFilter        : ~*, *.bak, *.tmp
        FolderState             : Initial Sync
        BacklogCount            : 286917
        BacklogReverseCount     : 53603
        BacklogCountSummary     : 340520
        ReplicationStatus       : False
        Status                  : True
        Error                   : False
        ErrorDescription        :

    .EXAMPLE
        'Get DFS-R groups, folders and connections in a second (skip backlog calculations) for the local server and export it to CSV'
        Get-RvDfsrReport -BacklogCount Skip -Remoting CIM | Export-Csv `
            -Path 'C:\Temp\My report.csv' `
            -Delimiter "`t" `
            -Encoding UTF8 `
            -NoTypeInformation

    .EXAMPLE
        'Display DFS-R report for multiple servers in a console'
        Get-RvDfsrReport -ComputerName fs0.ad.contoso.com, fs1.ad.contoso.com, fs2.ad.contoso.com |
            Format-Table -Property GroupName, FolderName, FolderState, BacklogCount, Status

    .INPUTS

    .OUTPUTS
        System.Management.Automation.PSCustomObject

    #>

    [CmdletBinding(
        DefaultParametersetName = 'ComputerName',
        SupportsShouldProcess = $true,
        PositionalBinding = $false,
        ConfirmImpact = 'Medium'
    )]

    Param
    (
        [Parameter(
            Mandatory = $false,
            Position = 0,
            ParameterSetName = 'ComputerName'
        )]
        [ValidateLength(1, 255)]
        [string[]]$ComputerName = '.',

        [Parameter(
            Mandatory = $false
            # Position = ,
            # ParameterSetName = ''
        )]
        [ValidateLength(1, 255)]
        [string]$GroupName = '*',

        [Parameter(
            Mandatory = $false
            # Position = ,
            # ParameterSetName = ''
        )]
        [ValidateLength(1, 255)]
        [string]$FolderName = '*',

        [Parameter(
            Mandatory = $false
            # Position = ,
            # ParameterSetName = ''
        )]
        [ValidateSet(
            'Skip',
            'Get',
            'BothDirections'
        )]
        [string]$BacklogCount = 'Get',

        [Parameter(
            Mandatory = $false
            # Position = ,
            # ParameterSetName = ''
        )]
        [int64]$BacklogCountError = 100,

        [Parameter(
            Mandatory = $false
            # Position = ,
            # ParameterSetName = ''
        )]
        [ValidateSet(
            'WMI',
            'CIM'
        )]
        [string]$Remoting = 'WMI'
    )

    Begin {
        # Configurations
        $ErrorActionPreference = 'Stop'
        if ($PSBoundParameters['Debug']) { $DebugPreference = 'Continue' }
        Set-PSDebug -Strict
        Set-StrictMode -Version Latest

        #region Functions
        Function Get-RvDfsrWmiOrCim {
            [CmdletBinding(
                DefaultParametersetName = 'ClassName',
                SupportsShouldProcess = $true,
                PositionalBinding = $false,
                HelpURI = 'https://techstronghold.com/',
                ConfirmImpact = 'Medium'
            )]

            Param
            (
                [Parameter(
                    Mandatory = $true,
                    Position = 0,
                    ParameterSetName = 'ClassName'
                )]
                [AllowNull()]
                [string]$ClassName,

                [Parameter(
                    Mandatory = $false
                    # Position = 0,
                    # ParameterSetName = ''
                )]
                [AllowNull()]
                [string]$Filter,

                [Parameter(
                    Mandatory = $false
                    # Position = 0,
                    # ParameterSetName = ''
                )]
                [AllowNull()]
                [string]$ComputerName = '.'
            )

            Begin {
                $error = $false
                $errorDescription = ''
                $parametersAndArguments = @{ }

                # Local (NetBIOS or FQDN) or remote device
                if ($ComputerName -and
                    $ComputerName -ne '.' -and
                    ($ComputerName -replace '\..*', '') -ne $env:COMPUTERNAME) {
                    $parametersAndArguments.Add('ComputerName', $ComputerName)
                }

                # Filter
                if ($Filter) {
                    $parametersAndArguments.Add('Filter', $Filter)
                }
            }

            Process {
                try {
                    if ($Remoting -eq 'WMI') {
                        $output = Get-WmiObject `
                            -Namespace ROOT\MicrosoftDfs `
                            -Class $ClassName `
                            -ErrorAction Stop `
                            @parametersAndArguments
                    }
                    else {
                        $output = Get-CimInstance `
                            -Namespace root/MicrosoftDfs `
                            -ClassName $ClassName `
                            -ErrorAction Stop `
                            @parametersAndArguments
                    }
                }
                catch {
                    $output = $null
                    $error = $true
                    $errorDescription = 'Device: {0}; WMI class {0}: Exception: {1}' -f $computerNameItem, $ClassName, $_.Exception.Message
                    Write-Warning -Message $errorDescription
                }

                if (!$output) {
                    $output = $null
                    $error = $true
                    $errorDescription = 'Device: {0}; WMI class {0}: No data' -f $computerNameItem, $ClassName
                    Write-Warning -Message $errorDescription
                }

                # Return
                [PsCustomObject]@{
                    Output           = $output
                    Error            = $error
                    ErrorDescription = $errorDescription
                }
            }

            End {
            }
        }

        Function Get-RvDfsrReportOutput {
            [CmdletBinding(
                DefaultParametersetName = 'Data',
                SupportsShouldProcess = $true,
                PositionalBinding = $false,
                HelpURI = 'https://techstronghold.com/',
                ConfirmImpact = 'Medium'
            )]

            Param
            (
                [Parameter(
                    Mandatory = $true,
                    Position = 0,
                    ParameterSetName = 'Data'
                )]
                $Data
            )

            Begin {
            }

            Process {
                $output = $Data

                if ($Data.ErrorDescription) {
                    $output.Status = $false
                    $output.Error = $true
                    $output.ErrorDescription = $Data.ErrorDescription -join '; '
                }
                else {
                    $output.ErrorDescription = $null
                }

                # Return
                $output
            }

            End {
            }
        }
        #endregion

        # Modify wildcards to WQL
        if ($GroupName -and $GroupName -ne '*') {
            $filterGroupName = $GroupName.Replace('*', '%').Replace('?', '_').Replace('\', '\\')
        }
        else {
            $filterGroupName = $null
        }

        if ($FolderName -and $FolderName -ne '*') {
            $filterFolderName = $FolderName.Replace('*', '%').Replace('?', '_').Replace('\', '\\')
        }
        else {
            $filterFolderName = $null
        }
    }

    Process {
        foreach ($computerNameItem in $ComputerName) {
            <#
            Variables
            #>

            $output = [PsCustomObject]@{
                DestinationComputerName = $computerNameItem
                SourceComputerName      = $null

                GroupName               = $null
                GroupGuid               = $null
                GroupDn                 = $null
                GroupIsClustered        = $null
                GroupScheduleInUtc      = $null

                FolderGuid              = $null
                FolderName              = $null
                FolderRootPath          = $null
                FolderEnabled           = $null
                FolderReadOnly          = $null
                FolderConflictSizeInMB  = $null
                FolderStagingSizeInMB   = $null
                FolderFileFilter        = $null

                # Normal, Initial replication, etc.
                FolderState             = $null

                # Backlog: Source -> Destination
                BacklogCount            = $null

                # Backlog: Destination -> Source
                BacklogReverseCount     = $null

                # Backlog: Sum of all directions
                BacklogCountSummary     = $null

                # If $false then replication is not in normal state or backlog is high
                ReplicationStatus       = $null

                # $false on any error during gtrial to get and process data
                Status                  = $true

                # $true on any error during gtrial to get and process data
                Error                   = $false
                ErrorDescription        = @()
            }



            <#
            Groups
            #>

            $parametersAndArguments = @{ }
            if ($filterGroupName) {
                $parametersAndArguments.Add('Filter', ("ReplicationGroupName LIKE '{0}'" -f $filterGroupName))
            }

            $groupConfigurationItems = Get-RvDfsrWmiOrCim `
                -ClassName 'DfsrReplicationGroupConfig' `
                -ComputerName $computerNameItem `
                @parametersAndArguments

            if ($groupConfigurationItems.Error) {
                Write-warning -Message 'Continue with another device'

                $output.ErrorDescription += $groupConfigurationItems.ErrorDescription

                # Return
                Get-RvDfsrReportOutput -Data $output
            }
            else {
                foreach ($groupConfigurationItem in $groupConfigurationItems.Output) {
                    <#
                    Group configurations
                    #>

                    try {
                        Write-Verbose -Message ('    - Group name: {0}' -f $groupConfigurationItem.ReplicationGroupName)

                        $output.GroupName = $groupConfigurationItem.ReplicationGroupName
                        $output.GroupGuid = $groupConfigurationItem.ReplicationGroupGuid
                        $output.GroupDn = $groupConfigurationItem.ReplicationGroupDn.Replace('\\', '\')
                        $output.GroupIsClustered = $groupConfigurationItem.IsClustered
                        $output.GroupScheduleInUtc = $groupConfigurationItem.DefaultScheduleInUtc
                    }
                    catch {
                        $message = 'Cannot get group configuration'
                        Write-warning -Message $message

                        $output.ErrorDescription += $message
                    }



                    <#
                    Folders
                    #>

                    $parametersAndArguments = @{ }
                    if ($filterFolderName) {
                        $filterAdd = " AND ReplicatedFolderName LIKE '{0}'" -f $filterFolderName
                    }
                    else {
                        $filterAdd = ''
                    }

                    $folderConfigurationItems = Get-RvDfsrWmiOrCim `
                        -ClassName 'DfsrReplicatedFolderConfig' `
                        -Filter ("ReplicationGroupGuid = '{0}'{1}" -f $groupConfigurationItem.ReplicationGroupGuid, $filterAdd) `
                        -ComputerName $computerNameItem

                    $connectionConfigurationItems = Get-RvDfsrWmiOrCim `
                        -ClassName 'DfsrConnectionConfig' `
                        -Filter ("Inbound = 'True' AND ReplicationGroupGuid = '{0}'" -f $groupConfigurationItem.ReplicationGroupGuid) `
                        -ComputerName $computerNameItem

                    if ($folderConfigurationItems.Error) {
                        Write-warning -Message 'Continue with another group'

                        $output.ErrorDescription += $folderConfigurationItems.Error

                        # Return
                        Get-RvDfsrReportOutput -Data $output
                    }
                    else {
                        foreach ($folderConfigurationItem in $folderConfigurationItems.Output) {
                            <#
                            Folder configurations
                            #>

                            try {
                                Write-Verbose -Message ('        - Folder name: {0}' -f $folderConfigurationItem.ReplicatedFolderName)

                                $output.FolderName = $folderConfigurationItem.ReplicatedFolderName
                                $output.FolderGuid = $folderConfigurationItem.ReplicatedFolderGuid
                                $output.FolderRootPath = $folderConfigurationItem.RootPath
                                $output.FolderEnabled = $folderConfigurationItem.Enabled
                                $output.FolderReadOnly = $folderConfigurationItem.ReadOnly
                                $output.FolderConflictSizeInMB = $folderConfigurationItem.ConflictSizeInMb
                                $output.FolderStagingSizeInMB = $folderConfigurationItem.StagingSizeInMb
                                $output.FolderFileFilter = $folderConfigurationItem.FileFilter
                            }
                            catch {
                                $message = 'Cannot get folder configuration'
                                Write-Warning -Message $message

                                $output.ErrorDescription += $message
                            }



                            <#
                            Folder information
                            #>

                            $folderInformationItem = Get-RvDfsrWmiOrCim `
                                -ClassName 'DfsrReplicatedFolderInfo' `
                                -Filter ("ReplicationGroupGUID = '{0}' AND ReplicatedFolderGuid = '{1}'" -f $groupConfigurationItem.ReplicationGroupGuid, $folderConfigurationItem.ReplicatedFolderGuid) `
                                -ComputerName $computerNameItem

                            if ($folderInformationItem.Error) {
                                $message = 'Cannot get folder information'
                                Write-Warning -Message $message

                                $output.ErrorDescription += $message
                            }
                            else {
                                try {
                                    switch ($folderInformationItem.Output.State) {
                                        0 { $output.FolderState = 'Uninitialized'; break }
                                        1 { $output.FolderState = 'Initialized'; break }
                                        2 { $output.FolderState = 'Initial Sync'; break }
                                        3 { $output.FolderState = 'Auto Recovery'; break }
                                        4 { $output.FolderState = 'Normal'; break }
                                        5 { $output.FolderState = 'In Error'; break }
                                        Default { $output.FolderState = 'Unknown' }
                                    }

                                    if ($folderInformationItem.Output.State -eq 4) {
                                        $output.ReplicationStatus = $true
                                    }
                                    else {
                                        $output.ReplicationStatus = $false
                                    }
                                }
                                catch {
                                    $message = 'Cannot get folder information'
                                    Write-warning -Message $message

                                    $output.ErrorDescription += $message
                                }
                            }



                            <#
                            Connections
                            #>

                            if ($connectionConfigurationItems.Error) {
                                Write-warning -Message 'Continue with another group'

                                $output.ErrorDescription += $connectionConfigurationItems.ErrorDescription

                                # Return
                                Get-RvDfsrReportOutput -Data $output
                            }
                            else {
                                foreach ($connectionConfigurationItem in $connectionConfigurationItems.Output) {
                                    $partnerComputerName = $connectionConfigurationItem.PartnerName

                                    Write-Verbose -Message ('            - Connection: {0} < - {1}' -f $computerNameItem, $partnerComputerName)

                                    $output.SourceComputerName = $partnerComputerName


                                    <#
                                    Backlog count
                                    #>

                                    if ($BacklogCount -ne 'Skip') {
                                        $folderInformationPartnerItem = Get-RvDfsrWmiOrCim `
                                            -ClassName 'DfsrReplicatedFolderInfo' `
                                            -Filter ("ReplicationGroupGUID = '{0}' AND ReplicatedFolderName = '{1}'" -f $groupConfigurationItem.ReplicationGroupGuid, $folderConfigurationItem.ReplicatedFolderName) `
                                            -ComputerName $partnerComputerName

                                        if ($folderInformationPartnerItem.Error) {
                                            Write-warning -Message 'Continue with another connection'

                                            $output.ErrorDescription += $folderInformationPartnerItem.ErrorDescription

                                            # Return
                                            Get-RvDfsrReportOutput -Data $output
                                        }
                                        else {
                                            <#
                                            Direction: Normal
                                            #>

                                            $errorBacklogDescription = $null

                                            try {
                                                $versionVector = $folderInformationPartnerItem.Output.GetVersionVector().VersionVector
                                            }
                                            catch {
                                                $errorBacklogDescription = 'Exception during trial to get version vector to get number of backlogs: {0}' -f $_.Exception.Message
                                                Write-Warning -Message $errorBacklogDescription
                                            }

                                            if (!$errorBacklogDescription) {
                                                try {
                                                    $output.BacklogCount = [int64]$folderInformationItem.Output.GetOutboundBacklogFileCount($versionVector).BacklogFileCount
                                                }
                                                catch {
                                                    $errorBacklogDescription = 'Exception during trial to get number of backlogs: {0}' -f $_.Exception.Message
                                                    Write-Warning -Message $errorBacklogDescription
                                                }
                                            }

                                            if ($errorBacklogDescription) {
                                                $output.ErrorDescription += $errorBacklogDescription
                                            }



                                            <#
                                            Direction: Reverse
                                            #>

                                            if ($BacklogCount -eq 'BothDirections') {
                                                $errorBacklogDescription = $null

                                                try {
                                                    $versionVector = $folderInformationItem.Output.GetVersionVector().VersionVector
                                                }
                                                catch {
                                                    $errorBacklogDescription = 'Exception during trial to get version vector to get number of backlogs in reverse direction: {0}' -f $_.Exception.Message
                                                    Write-Warning -Message $errorBacklogDescription
                                                }

                                                if (!$errorBacklogDescription) {
                                                    try {
                                                        $output.BacklogReverseCount = [int64]$folderInformationPartnerItem.Output.GetOutboundBacklogFileCount($versionVector).BacklogFileCount
                                                    }
                                                    catch {
                                                        $errorBacklogDescription = 'Exception during trial to get number of backlogs in reverse direction: {0}' -f $_.Exception.Message
                                                        Write-Warning -Message $errorBacklogDescription
                                                    }
                                                }

                                                if ($errorBacklogDescription) {
                                                    $output.ErrorDescription += $errorBacklogDescription
                                                }
                                            }



                                            <#
                                            Direction: Summary
                                            #>

                                            if ($output.BacklogCount -ne $null -and $output.BacklogReverseCount -ne $null) {
                                                $output.BacklogCountSummary = $output.BacklogCount + $output.BacklogReverseCount
                                            }



                                            <#
                                            Replication status
                                            #>

                                            if ($output.BacklogCount -gt $BacklogCountError -or $output.BacklogReverseCount -gt $BacklogCountError) {
                                                $output.ReplicationStatus = $false
                                            }
                                        }
                                    }

                                    # Return
                                    Get-RvDfsrReportOutput -Data $output
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    End {
    }
}