# DFS manipulation with PowerShell
<#
 With Server 2008 Microsoft implemented Access Based Enumeration 
 (ABE) to DFS but you have to migrate your namespace to 
 a Windows Server 2008 mode to use this feature. This means
 that you have to recreate your namespace.  Doing this via the 
 GUI could be a real pain if your servers are hosting many or 
 very large namespaces.
#>

<#
.SYNOPSIS
This script recreates DFS Namespaces in Server 2008 mode with DNS only
.DESCRIPTION
This script recreates DFS Namespaces in Server 2008 mode in a DNS only environment.
#>

# Module

Import-Module ActiveDirectory

# Import all DFS Roots hosted by this server that are not standalone

$dfsnRoots = Get-DfsnRoot -ComputerName $env:computername | Where type -NotMatch "Standalone"

# Do for all DFS Roots on the local Server

foreach ($root in $dfsnRoots) {

    #Remember servers
    $serverList = Get-DfsnRootTarget -Path $root.path
  
    #How many servers?
    $serverCounter = $serverList.Count
  
    # Get name of namespace
    $backuptarget = "C:\temp" + ($root.path).Replace("", "-") + ".xml"
    New-Item -ItemType Directory -Force -Path C:\temp
    dfsutil.exe root export $root.path $backuptarget
  
    #Prompt to alter the Backup file (FQDN)
    $message = "Please edit the following export and change NETBIOS names to FQDN: " + $backuptarget + " Press    any key to continue..."
    Write-Host -NoNewLine $message
    $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
    $localTargetPath = ""
  
    #Remove all other namespace servers and activate FQDN
    foreach ($namespaceserver in $serverlist) {
        if (!(($namespaceserver.TargetPath).Contains($env:computername)) ) {
            Remove-DfsnRootTarget -TargetPath $namespaceserver.TargetPath -Path $root.path
            $ausgabe = "Removed " + $namespaceserver.TargetPath
            echo $ausgabe
        }
        if (($namespaceserver.TargetPath).Contains($env:computername) ) {
            $localTargetPath = $namespaceserver.TargetPath
            $ausgabe = "localTargetPath " + $localTargetPath
            echo $ausgabe
        }
  
        # Get hostname from $namespaceserver URI
        $hntemp = ($namespaceserver.TargetPath).Replace("\", "")
        $end = $hntemp.IndexOf("")
        $hn = $hntemp.SubString(0, $end)
  
        #Set DFS FQDN parameter
        Set-DfsnServerConfiguration -ComputerName $hn -UseFqdn $true
  
        # DNS only Domain Config
        if (!(($namespaceserver.TargetPath).Contains($env:computername)) ) {
            Try {
                $s = New-PSSession -ComputerName $hn -ErrorAction Stop
                Invoke-Command $s -ScriptBlock { Param($path)dfsutil server registry DfsDnsConfig set $path } -ArgumentList
                $root.path | Out-Null
                Remove-PSSession $s
            }
            Catch {
                Write-Host "Remote Server connection error"
            }
        }
        else {
            dfsutil server registry DfsDnsConfig set $root.path
        }

    }

    #Replicate changes
    repadmin /syncall
    dfsrdiag pollad
  
    #Remove root
    Remove-DfsnRoot -Path $root.path
  
    #Replicate changes
    repadmin /syncall
    dfsrdiag pollad
  
    # Restart Dfs
    Stop-Service dfs;
    Start-Service dfs
    Start-Sleep -s 5
  
    # Restore Namespace as Server 2008 version
    New-DfsnRoot -TargetPath $localTargetPath -Type DomainV2 -Path $root.path
  
    #Replicate changes
    repadmin /syncall
    dfsrdiag pollad
  
    #Add remaining targets
    foreach ($namespaceserver in $serverlist) {
        if (!(($namespaceserver.TargetPath).Contains($env:computername)) ) {
            New-DfsnRootTarget -Path $root.path -TargetPath $namespaceserver.TargetPath
            $output = "Added " + $namespaceserver.TargetPath + " to " + $root.path
            echo $output
        }
    }
  
    #Import backup
    dfsutil.exe root import set $backuptarget $root.path
}