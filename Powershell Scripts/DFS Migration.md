# Migrating your DFS Namespaces in three (sorta) easy steps

#### January 15, 2008 by NedPyle

Hi, Dave here. Today, I will cover the process by which domain DFS namespaces can be migrated from one domain to another, important considerations both during and after the migration, and some helpful tips along the way.
My post assumes that you have some working knowledge of DFS and related terminology. Don’t worry if you are new to DFS… we have excellent documentation over on the Windows 2003 Server Technical Reference website. I’ll wait right here until you get back.

To begin with, we know that DFS is used to build a unified namespace for files scattered throughout your Windows environment. This way, users don’t need to know which servers contain their data and the names of any particular share. They only need to know the root of your DFS namespace to begin locating their files and get silently referred to the required file server. This is all well and good, but what happens when you move your files shares to a new domain or environment and want bring your elaborate DFS namespace along with the data? Or what if you simply wish to make another copy of an existing DFS namespace? The answer is with the DFSUTIL.exe support tool.

DFSUTIL is a command-line tool provided within the Windows Server 2003 Support Tools package. With it, you can export a specified DFS namespace to an XML text file and later import this information back into a new DFS root.
Before using these commands, ensure that you have the latest version of the Support Tools installed on your system where you will be exporting/importing the DFS configuration. Please note the process by which the data or file servers are migrated between the environments is beyond the scope of this blog.
It is also recommended to create a full system-state backup of your domain controller(s). This way, any accidental deletions or overwrites of your DFS configuration can be easily recovered.

The steps below detail the process by which a DFS root called “public” was migrated from the domain “contoso.com” to a new “public” root in the domain “fabrikam.com”. A two-way trust exists between these domains and network communications between them is fully functional. Although this environment is simplistic, the process is applicable to namespaces with hundreds of folders and targets.
Here is a screenshot of the Public namespace within contoso.com:

## Step1 – Exporting a Namespace:

The command to export the namespace is `“dfsutil /root:\\domain.com\rootname /export:exportedroot.txt /verbose`

As you can see, I exported my domain DFS root named “public” to a file named “publicroot.txt”. My root happens to contain 3 folders, named “accounting”, “utilities”, and “documentation”. “Accounting” has two folder targets, and “utilities” and “documentation” each have a single folder target. All target file servers, FS1 and FS2, are in the Contoso.com domain.

The publicroot.txt file contains:
```
<Root Name=”\\CONTOSO\Public” State=”1″ Timeout=”300″ Attributes=”64″ > 
    <Target Server=”CONTOSOROOT1″ Folder=”Public” State=”2″ /> 
    <Target Server=”CONTOSOROOT2″ Folder=”Public” State=”2″ /> 
    <Link Name=”Accounting” State=”1″ Timeout=”1800″ > 
        <Target Server=”fs1″ Folder=”accounting” State=”2″ /> 
        <Target Server=”fs2″ Folder=”accounting” State=”2″ /> 
    </Link> 
    <Link Name=”utilities” State=”1″ Timeout=”1800″ > 
        <Target Server=”fs1″ Folder=”utilities” State=”2″ /> 
    </Link> 
    <Link Name=”documentation” State=”1″ Timeout=”1800″ > 
        <Target Server=”fs2″ Folder=”documentation” State=”2″ /> 
    </Link> 
</Root>

```
There, that was easy enough! Now that the root has been exported, some edits to this data is required before import.


## Step 2 – Editing the configuration file
First off, you see that the “root name” value is “\\CONTOSO\Public”. Because the root configuration needs to be imported into the Fabrikam domain, this must be manually modified. The modified portion of the namespace file will look like this:

`<?xml version=”1.0″?>
<Root Name=”\\FABRIKAM\Public” State=”1″ Timeout=”300″ Attributes=”64″ >`

The remainder of the file will remain untouched, for reasons which will be discussed below. This file should be saved (I named it publicrootmodified.txt)

## Step 3 – Create the new namespace in the new environment/domain

Before a DFS configuration file can be imported, the target namespace must be manually created—DFSUTIL won’t create the root for you.
The command to import the configuration is as follows:

`dfsutil /root:\\domain.com\rootname /import: publicrootmodified.txt /set /verbose`

*NOTE! The import process will overwrite any DFS configurations in the target namespace. Please ensure you enter the path of a root you are prepared to replace.
If you try an import without first creating the DFS root, you will get the following error:*

```
System error 1168 has occurred. 
Element not found.

```
Likewise, attempting to import the configuration file before changing the “Root Name” value within it to match the namespace will result in the error:

`System error 2 has occurred. 
The system cannot find the file specified.`

A successful import will appear as follows:

The new DFS namespace in the fabrikam domain:

*Notice how the root targets “CONTOSOROOT1” and “CONTOSOROOT2” don’t show up under the “Namespace Servers” tab.* 

This is because DFSUTIL ignores any root targets listed in the configuration file. You have the option to configure additional namespace servers in the DFS Management tool either before or after you import the configuration file. In my example, I had a single namespace server in the Fabrikam domain called **“fabrikamroot1”**.
If you take a peek at the dfsutil.exe command syntax, you may notice there is also a “merge” option in addition to “set”. Merge can only be utilized if your configuration XML specifies folders and targets which are not already present in the namespace. This may be useful if you want to incrementally import portions of the namespace, but requires careful manipulation of the XML configuration files and isn’t generally recommended.

Let’s take a few moments to review what we have done. First, we exported DFS configuration information, changed the value for the new namespace/root name, and then imported it into a new namespace. Because of the domain trust, clients in both domains can now seamlessly access any of the 3 folders via either the “\\contoso.com\pubic” or “\\fabrikam.com\public” namespaces — both namespaces will issue referrals to the folder targets which still reside in the consoto.com domain. 

It is likely that your migration requires making the shared data part of the other domain. Through beyond the scope of this blog post, this may entail simply joining file servers to the other domain, copying the data to a completely new server in the other domain, consolidating many target folders to a single file server in the other domain, or using a domain migration tool such as the Active Directory Migration Tool (ADMT) to migrate the server(s).

Lastly, here are a number of considerations to ensure this process goes smoothly:
Don’t enable FRS or DFSR replication until the folder targets all exist within the same domain or forest, otherwise it won’t work.
Using dfsutil.exe to migrate namespaces doesn’t preserve FRS or DFSR replication configurations.

If after importing the namespace clients have problems accessing the namespaces or any of the folders, check to see if they can directly access the root and folder targets via \\server\share to determine if the namespace or something else is at fault.

Access to resources between the domains is highly dependant on the health of the domain trust–verify the trust’s status and ensure name resolution is functioning correctly.

If any folder (link) target server names or share names are changed, the migrated namespaces will need to be manually updated to reflect this. This is most likely to happen if DFS is configured to use DNS names rather than NetBIOS names and file servers are moved to the other domain.

DFS configuration changes may not be immediate. Client’s cache referral information which won’t be updated until it expires. Additionally, Active Directory replication latencies may also cause namespace servers to only detect changes after they poll domain controllers for changes (60 minutes by default).

Also note that the steps detailed here can be applied to standalone DFS Namespace servers. The process of exporting, modifying, and then importing the namespace will be much the same.

And there you have it — a complete migration of DFS configuration in 3 easy steps. They should prove useful when wishing to rename a namespace, making a copy of the namespace for use in a test environment, and backing up the namespace in the event that the namespace is accidentally deleted or modified.

– David Fisher