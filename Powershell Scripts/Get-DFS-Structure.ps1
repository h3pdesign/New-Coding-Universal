function Get-DFS-Structure {

<#
param([string]$folderpath = "\\gll\gll-abl")  
   
 $erroractionpreference = "silentlycontinue"  
 Import-module DFSN
 Import-module dfsutil
 $arr = $folderpath.split("\\")  
 $basepath = ("\\" + $arr[2] + "\" + $arr[3])  
 $testpath = $basepath  
   
 # go from the 4th element of the path and try to get the target of each
 for($i = 1; $i -lt $arr.count; $i++){  
    $testpath = $testpath + "\" + $arr[$i]  
    $result = get-dfsnfoldertarget $testpath  
    $testpath + "->" + $result.targetpath  
   
    if($result.targetpath){  
       $testpath = $result.targetpath  
    }  
 } 
 }

#>

 #Get-DFS-Structure "\\gll\gll-abl\"
 #Get-DFS-Structure "\\gll.ads.niedersachsen.de"
 #Get-DFS-Structure "\\fileserver-hm.gll.ads.niedersachsen.de"

[CmdletBinding()]
param(
$DfsProvider = "gll-h2-fs61",
$DfsPath = "\\gll.ads.niedersachsen.de"
)

Get-WmiObject -ComputerName $DfsProvider -Class Win32_DFSTarget `
-Filter "SELECT ServerName,ShareName,LinkName FROM Win32_DFSTarget WHERE LinkName = '$DfsPath'"

}

#dfsutil client property state $DFSPath