function Get-Longpaths {  
  <#   
.SYNOPSIS   
  Retrieves a list of the paths that are too long for being managed with get-childitem.  
    
.DESCRIPTION   
  Retrieves a list of the paths that are too long for being managed with get-childitem.  
  An object is returned containing the list of the paths longer then 260 characters.  
    
.PARAMETER Path  
  The parent path that you need to recursively check.  
  
.PARAMETER Csvpath
  The name of the csv log file you optionally want to export your list of long paths to.  
  
.EXAMPLE  
  For Console: .\Get-Longpaths.ps1  
  Get-Longpaths C:\  
  Retrieves long path on the system partition c: and show on the current host.  
  Get-Longpaths "C:\Temp" C:\longpathnames.csv -verbose 

.EXAMPLE  
  Get-Longpaths C:\Documents C:\Logs\longpathnames.csv -verbose  
  Retrieves long path inside the folder C:\documents and saves the  
  output to a csv file named longpathnames.csv under C:\Logs\.  
  It also shows additional information on the task being performed.  
#>  
  [CmdletBinding()]  
  
  param(  
    [Parameter(Mandatory = $true)]  
    [string] $Path,  
    [Parameter(Mandatory = $false)]  
    [string] $csvlog  
  )  
  

  #Retrieving path

  $options = [system.IO.SearchOption]::AllDirectories  
  $allfiles = [system.IO.Directory]::GetFiles($path, "*", $options)  
  $allfolders = [system.IO.Directory]::GetDirectories($path, "*", $options)  
  $toolongcontainer = @()  
  


  foreach ($file in $allfiles) {  
    if ($file.Length -gt 256) {  
      write-verbose "Adding $file to the list of too long paths"  
      $toolongcontainer += $file  
    }  
  }  
  
  foreach ($folder in $allfolders) {  
    if (($folder | out-string).Length -gt 256) {  
      write-verbose "Adding $folder to the list of too long paths"  
      $toolongcontainer += $folder  
    }  
  }  
    
    
  # Progressbar
  For ($i = 1; $i -le $folder.count; $i++) {  

    #$i =($i / $folder.count*100)
    Write-Progress -Activity "Collecting paths here" 
    -PercentComplete (($i * 100) / $folder.count) 
    -Status "Finding path $($folder[$i].name)"
    Start-sleep -Milliseconds 100
  }
    
    
  if (!($toolongcontainer)) {  
    write-verbose "No too long paths found. Good."  
    $toolongcontainer = "No invalid path under $path"  
  }  
  if ($csvlog) {  
    write-verbose "Exporting output to $csvpath"  
    $toolongcontainer | Export-Csv -Path $csvpath -NoTypeInformation -USECULTURE -ErrorAction Stop   
  }  
  return $toolongcontainer  
    



}  
  
Get-Longpaths E:\Intranet C:\Logs\longpathnames.csv -verbose -ErrorAction SilentlyContinue

Get-WmiObject