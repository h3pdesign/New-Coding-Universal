# How to for Managed Distributed File System (DFS) Links with PowerShell

Monday, March 23, 2015 4:40 PM

Distributed File System (DFS) Links reduce the complexity of working with network file shares. DFS Links allow users and applications to access a “virtual path name” to connect to shared folders. We can create DFS links with PowerShell.

This “virtual namespace” enables administrators to present shared folders located on different servers, or even change a shared folder’s location, completely transparent to that folder’s consumers.

Users will not need to update bookmarks, and applications will not be required to be updated with new paths when File Servers change.

For the users, access to network share folders is simplified down to a “namespace\FolderName” format, a reduction in the complexity associated with folders stored on remote servers.

## Benefit to Applications

For applications, hard-coded paths to resources on the network do not have to be changed due to a change in the network path. A simple update to the DFS Link and the application will continue to access the resources at their new location.

## Prerequisites for the DFS Server Role

- Active Directory
- File and Storage Services role installed on a Windows Server:
- Windows Server (Semi-Annual Channel)
- Windows Server 2016
- Windows Server 2012 R2
- Windows Server 2012
- Windows Server 2008 R2 Datacenter/Enterprise

## Prerequisites for PowerShell cmdlets:

- An administrator account with the proper permissions
- RSAT Tools with the ‘File Services Tools – DFS Management Tools’ installed

## Enabling DFS Tools with PowerShell

[Download and install RSAT](https://www.microsoft.com/en-us/download/details.aspx?id=45520)
Next, you need to Enable the *Distributed File System Tools*and 
- open PowerShell as an Administrator
- Run the Install-WindowsFeature command:

## How to Set Up DFS with PowerShell

We first need to install all of the necessary Windows features. This will install DFS Management GUI, the DFS Namespaces module for **Windows PowerShell** to create DFS links with PowerShell and manage them, and command-line tools, but it does not install any DFS services on the server.

    **Install-WindowsFeature FS-DFS-Namespace, RSAT-DFS-Mgmt-Con**

## Administration of DFS Links

You can administer namespaces by using DFS Management GUI, the DFS Namespace (DFSN) Cmdlets in Windows PowerShell, the DfsUtil commands, or scripts that call WMI.

## Common PowerShell commands

`Get-DfsnRoot` – Discover all DFS Namespaces in the current domain*– Commonly used to check for available namespaces in the current domain*

`New-DfsnFolder` – Create a new DFS Folder Name*– Commonly used to create a new DFS Folder in a NameSpace*

`New-DfsnFolderTarget` – Assign path(s) to a DFS Folder Name*– Commonly used to assign one or more network folder paths to a DFS Folder*

`Remove-DfsnFolderTarget` – Removes a path from a DFS Folder but does not remove the DFS Folder.*– Commonly used to remove one or more network folder paths from a DFS Folder*

`Remove-DfsnFolder` – Removes a folder and all its paths*– Commonly used to remove a DFS Folder from a NameSpace*

## Finding DFS namespaces with PowerShell

We’ll start out by getting an idea of all the online and available NameSpaces in the current Domain using the cmdlet Get-DfsnRoot.

    $Domain = 'tech.io'
    (Get-DfsnRoot -Domain $Domain).Where( {$_.State -eq 'Online'} ) | Select-Object -ExpandProperty Path

From this output, we can see that in the AppRoot NameSpace this is not a DFS Folder named PowerShell.

![Output](/Image&#32;Resources/img_5b68754740ec71-b19aafe0-e06b-4bf8-8069-5dc3bf896075.png)

This shows that there are two NameSpaces that are Online in this domain.

    $Domain = '[tech.io](http://tech.io/)'
    Get-DfsnFolder -Path "\\$Domain\AppRoot\*" | Select-Object -ExpandProperty Path
    Get-DfsnFolder -Path "\\$Domain\DFSRoot\*" | Select-Object -ExpandProperty Path

![Output](/Image&#32;Resources/img_5b687471dfa051-32c09988-3d12-4916-b71e-0c9218ebfe4c.png)

## Creating DFS Link Folders with PowerShell

In this example, we have a replicated folder named `PowerShell` on our 3 File Services servers
* FileServer01
* FileServer02
* Datacenter

The goal is to share this replicated folder with our Admins using a single path.

To do this, we’ll create a new DFS Link folder in the **AppRoot** NameSpace called ***PowerShell*** using `New-DfsnFolder` and point it to the Datacenter server’s FileShare, set the DFS Folder State to **Online** and set the TargetPath state to **Online**.

    $Domain = '[tech.io](http://tech.io/)'
    try {
    Get-DfsnFolderTarget -Path "\\$Domain\AppRoot\PowerShell" -ErrorAction Stop
    } catch {
    Write-Host "Path not found. Clear to proceed" -ForegroundColor Green
    }

    $NewDFSFolder = @{
    Path = "\\$Domain\AppRoot\PowerShell"
    State = 'Online'
    TargetPath = '\\datacenter\FileShare\PowerShell'
    TargetState = 'Online'
    ReferralPriorityClass = 'globalhigh'
    }
    
    New-DfsnFolder @NewDFSFolder
    #Check that folder now exists:
    Get-DfsnFolderTarget -Path "\\$Domain\AppRoot\PowerShell"
    #Check that the new DFS Link works using Windows Explorer
    Invoke-Expression "explorer '\\$Domain\AppRoot\PowerShell\'"

Run PowerShell and check for the DFS FolderTargetPath

`\\Tech.io\AppRoot\PowerShell` – if it doesnt exist it will write the output ‘Path not found. Clear to proceed’ in green text in the terminal window.

From the output we see that:
* Path has been created
* Referral Priority Class is set to `Global-High`
* State is `Online`

The GUI confirms what PowerShell told us.

## Creating DFS Folder Targets with PowerShell

Now that we successfully created the “Powershell” DFS Folder in our NameSpace, we’re going to add an additional Folder Target Path to it and set that path as **Online** using `New-DfsnFolderTarget`.

    **$Domain = 'tech.io'
    # Splat the settings for easy readibility
    $NewTPS = @{
    Path = "\\$Domain\AppRoot\PowerShell"
    TargetPath = '\\FileServer01\FileShare\PowerShell'
    State = 'Online'
    }
    # Add new folder located on the 'FileServer01' server &amp; set Online
    New-DfsnFolderTarget @NewTPS
    # Check that folder now exists:
    Get-DfsnFolderTarget -Path "\\$Domain\AppRoot\PowerShell"**

Up to this point, we have two of our three Server Paths added, and online. For our last Folder Path, we want to add the path but not make it available to users. So let’s add a Folder Target Path to our “PowerShell” DFS Folder and this time set the DFS Folder Path State to **Offline** we will again use `New-DfsnFolderTarget`

    **$Domain = 'tech.io'
    # Splat the settings for easy readibility
    $NewTPS = @{
    Path = "\\$Domain\AppRoot\PowerShell"
    TargetPath = '\\FileServer02\FileShare\PowerShell'
    State = 'Offline'
    }
    # Add new folder located on the 'FileServer02' server &amp; set to Offline
    New-DfsnFolderTarget @NewTPS
    # Check that folder now exists:
    Get-DfsnFolderTarget -Path "\\$Domain\AppRoot\PowerShell"**

FileServer01 and Datacenter’s path is currently `Online`
FileServer02‘s state has been set to `Offline`

## Setting DFS Folders Targets to Offline or Online with PowerShell

We can change which servers are the *Online* and *Offline* hosts, and even which will be our server will be the primary host of the file path using `Set-DfsnFolderTarget`.

    **$Domain = 'tech.io'
    # Splatting the settings where the path pointed at the server named FileServer01
    $ChangeTPsFS1 = @{
    Path = "\\$Domain\AppRoot\PowerShell"
    TargetPath = '\\FileServer01\FileShare\PowerShell'
    State = 'Offline'
    }
    # Set folder located on the server path 'FileServer01' to Offline
    Set-DfsnFolderTarget @ChangeTPsFS1
    # Splatting the settings where the path pointed at the server named FileServer02
    $ChangeTPsFS2 = @{
    Path = "\\$Domain\AppRoot\PowerShell"
    TargetPath = '\\FileServer02\FileShare\PowerShell'
    State = 'Online'
    ReferralPriorityClass = 'globalhigh'
    }
    # Set folder located on the 'FileServer02' server to Online
    Set-DfsnFolderTarget @ChangeTPsFS2
    # Splatting the settings where the path pointed at the server named Datacenter
    $ChangeTPsFS3 = @{
    Path = "\\$Domain\AppRoot\PowerShell"
    TargetPath = '\\datacenter\FileShare\PowerShell'
    ReferralPriorityClass = 'sitecostnormal'
    }
    # Change Priority of 'Datacenter' server folder path to 'Normal'
    Set-DfsnFolderTarget @ChangeTPsFS3
    # Check folder:
    Get-DfsnFolderTarget -Path "\\$Domain\AppRoot\PowerShell"**

As you can see below in the ScreenCap FileServer01‘s path has changed to `Offline`Datacenter server’s ReferralPriorityClass has switched to `sitecost-normal` from `global-high`
Also, notice that FileServer02‘s path has changed its state to `Online` and its ReferralPriorityClass has switched to `global-high`

![output](/Image&#32;Resources/img_5b6875250c9d81-394dcc8b-6820-42f0-b666-543149da1230.png)

## Removing DFS folder target paths with PowerShell

I try to vaccinate my code against the ***Fat Finger Flu*** as much as possible. Here we will try to install a “Safety Net” before removing one of the FolderTargetPaths by making sure that it is at least `Offline` before deleting it.

    **# Check Target Path to 'FileServer01' server to Offline &amp; Remove the Folder Target Path
    if ((Get-DfsnFolderTarget -Path "\\$Domain\AppRoot\PowerShell" -TargetPath '\\FileServer01\FileShare\PowerShell').State -eq "Offline") {
    Remove-DfsnFolderTarget -Path "\\$Domain\AppRoot\PowerShell" -TargetPath '\\FileServer01\FileShare\PowerShell' -Force:$true
    }
    # Check folder:
    Get-DfsnFolderTarget -Path "\\$Domain\AppRoot\PowerShell"**

So long path FileServer01

![Output](/Image&#32;Resources/img_5b687534e4c781-c263ad0a-aa73-48f3-9346-fff7e977b6e3.png)

For those who prefer to “cowboy” it up and forego the “safety net” option, we can accommodate you, brave souls, also.

    **$Domain = 'tech.io'
    # Splatting the settings where the path pointed at the server named 'FileServer02'
    $DelFTS = @{
    Path = "\\$Domain\AppRoot\PowerShell"
    TargetPath = '\\FileServer02\FileShare\PowerShell'
    }
    # Delete the DFS FolderTarget
    Remove-DfsnFolderTarget @DelFTS -Force:$true
    # Check the settings
    Get-DfsnFolderTarget -Path "\\$Domain\AppRoot\PowerShell"**
    

We’ve bid adieu to the path to FileServer02

![Output](/Image&#32;Resources/img_5b68754740ec71-b19aafe0-e06b-4bf8-8069-5dc3bf896075.png)

## Removing DFS Folders with PowerShell

It’s has been a long and winding path, but the time for our DFS Link has come to an end. We can Remove the PowerShell folder, DFS Link, using Remove-DfsnFolder.

    **$Domain = 'tech.io'
    # Delete the DFS Folder
    Remove-DfsnFolder -Path "\\$Domain\AppRoot\PowerShell" -Force:$true
    # Final Check
    Get-DfsnFolderTarget -Path "\\$Domain\AppRoot\PowerShell"
    12345678$Domain = 'tech.io' # Delete the DFS FolderRemove-DfsnFolder -Path "\\$Domain\AppRoot\PowerShell" -Force:$true # Final CheckGet-DfsnFolderTarget -Path "\\$Domain\AppRoot\PowerShell"** 

![Output](https://i2.wp.com/blog.techsnips.io/wp-content/uploads/2018/08/img_5b687558e2b5d.png?w=1098&ssl=1)

A quick double-check of the DFS Management GUI shows our DFS Link is no more.

## DFS Folder Cmdlets

    New-DfsnFolder -Path "\\<DFS_ROOT>\data\it\imaging\<USERNAME>" -TargetPath "\\<SERVER>\<SHARE>\<USERNAME>"

Instead of getting the correct target, what I actually get is "\\<SERVER>\<SHARE>". In other words it chops off the "<USERNAME>" at the end. The path is always correct, but the target is always wrong, so if I script this for 400 users the folders are all created but they all point at the folder above!

![Output](/Image&#32;Resources/Untitled-b88dce47-e1ec-47e4-bab4-46f033994533.png)

You can see after running the cmdlet in PowerShell, both Powershell and DFS management show the correct result.

Thus in your current situation it seems to be a network issue, that when trying to access \\server\share\username folder, it can only connect to \\server\share.

You mentioned that you tried to create a new share on Drive C and the same issue persists. Please try again with creating a c:\folder, which Everyone - Full Control in both Share and NTFS permission (Share tab and Security tab). Create a subfolder under c:\folder and redo the test to see the result.

    New-DfsnFolder -Path \\server\data\it\imaging\howard -TargetPath \\my_workstation\howard\mydata\

run the following:

    Get-DfsnFolder -Path [\\server\data\it\imaging\howard](file://server/data/it/imaging/howard) | Get-DfsnFolderTarget | fl *

which reports:

    Path :[\\server\data\it\imaging\howard](file://server/data/it/imaging/howard)
    
    State : Online
    ReferralPriorityClass : sitecost-normal
    NamespacePath :[\\server\data\it\imaging\howard](file://server/data/it/imaging/howard)
    
    ReferralPriorityRank : 0
    TargetPath :[\\my_workstation\howard](file://my_workstation/howard)
    
    PSComputerName :
    CimClass : ROOT/Microsoft/Windows/DFSN:MSFT_DfsNamespaceFolderTarget
    CimInstanceProperties : {NamespacePath, ReferralPriorityClass, ReferralPriorityRank, State...}
    CimSystemProperties : Microsoft.Management.Infrastructure.CimSystemProperties

Note that the target path does not reference the "mydata" folder beneath the "howard" share.

    Get-DfsnFolder -Path \\server\data\it\imaging\howard | Get-DfsnFolderTarget | fl *

Output:

    Path :
    [\\server\data\it\imaging\howard](file://server/data/it/imaging/howard)
    State : Online
    ReferralPriorityClass : sitecost-normal
    NamespacePath : 
    [\\server\data\it\imaging\howard](file://server/data/it/imaging/howard)
    ReferralPriorityRank : 0
    TargetPath : 
    [\\my_workstation\howard\mydata](file://my_workstation/howard/mydata)
    PSComputerName :
    CimClass : ROOT/Microsoft/Windows/DFSN:MSFT_DfsNamespaceFolderTarget
    CimInstanceProperties : {NamespacePath, ReferralPriorityClass, ReferralPriorityRank, State...}
    CimSystemProperties : Microsoft.Management.Infrastructure.CimSystemProperties

It doesn't seem to be a permissions thing to me. It works perfectly through the GUI but I don't fancy creating over 400 of these things when my script will do this in a few seconds, however at this point all it would do is point all of the user folders at the share and not their unique folder below which is far from useful. ;-)