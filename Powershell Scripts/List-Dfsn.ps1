<#
.Synopsis
   Inventory Distributed File System (DFS) namespaces
.DESCRIPTION
   The List-Dfsn cmdlet extends Get-DfsnRoot cmdlet to not only list DFS Namespaces, but DFS targets too (Share names, Share local paths and target servers)

   The cmdlet gets all Get-DfsnRoot parameters and two new parameters: IncludeSMBShares and SkipAccessErrors
.EXAMPLE
   List-Dfsn
   
   List DFS Namespaces as Get-DfsnRoot
.EXAMPLE
   List-Dfsn -IncludeSMBShares
   
   List DFS Namespaces, targets, shares and servers
.EXAMPLE
   List-Dfsn -IncludeSMBShares:$true -SkipAccessErrors | Export-Csv dfs-inv.txt -NoTypeInformation
   
   As previous with suppress error messages (WinRM, access denied and so on) and export to CSV file
.INPUTS
   The cmdlet get Get-DfsnRoot's parameters plus two new parameters: IncludeSMBShares and SkipAccessErrors
.OUTPUTS
   Output 
        1. (Default) list of DFS Namespaces as Get-DfsnRoot
        2. or (IncludeSMBShares) DFS Namespaces and DFS folder targets with Share names, Share local paths and target servers
#>
function List-Dfsn
{

    [CmdletBinding(DefaultParameterSetName='ByDomain', PositionalBinding=$false, HelpUri='http://go.microsoft.com/fwlink/?L
    inkID=239839')]
    param(
        [Parameter(ParameterSetName='ByRoot', Position=0, ValueFromPipelineByPropertyName=$true)]
        [Alias('RootPath','root','namespace','NamespaceRoot')]
        [ValidateNotNullOrEmpty()]
        [ValidateNotNull()]
        [string]
        ${Path},

        [Parameter(ParameterSetName='ByDomain', Position=0, ValueFromPipelineByPropertyName=$true)]
        [ValidateNotNullOrEmpty()]
        [ValidateNotNull()]
        [string]
        ${Domain},

        [Parameter(ParameterSetName='ByServer', Position=0, ValueFromPipelineByPropertyName=$true)]
        [Alias('Server')]
        [ValidateNotNullOrEmpty()]
        [ValidateNotNull()]
        [string]
        ${ComputerName},

        [Parameter(ParameterSetName='ByServer')]
        [Parameter(ParameterSetName='ByDomain')]
        [Parameter(ParameterSetName='ByRoot')]
        [Alias('Session')]
        [ValidateNotNullOrEmpty()]
        [Microsoft.Management.Infrastructure.CimSession[]]
        ${CimSession},

        [Parameter(ParameterSetName='ByServer')]
        [Parameter(ParameterSetName='ByDomain')]
        [Parameter(ParameterSetName='ByRoot')]
        [int]
        ${ThrottleLimit},

        [Parameter(ParameterSetName='ByServer')]
        [Parameter(ParameterSetName='ByDomain')]
        [Parameter(ParameterSetName='ByRoot')]
        [switch]
        ${AsJob},
        
        # Suppress error messages in output
        [Parameter(ParameterSetName='ByServer')]
        [Parameter(ParameterSetName='ByDomain')]
        [Parameter(ParameterSetName='ByRoot')]
        [switch]
        $SkipAccessErrors = $false,

        # Include DFS folder targets with Share names, Share local paths and target servers
        [Parameter(ParameterSetName='ByServer')]
        [Parameter(ParameterSetName='ByDomain')]
        [Parameter(ParameterSetName='ByRoot')]
        [switch]
        $IncludeSMBShares = $true
        )

    begin
    {
        try {
            $outBuffer = $null
            if ($PSBoundParameters.TryGetValue('OutBuffer', [ref]$outBuffer))
            {
                $PSBoundParameters['OutBuffer'] = 1
            }
            $wrappedCmd = $ExecutionContext.InvokeCommand.GetCommand('Get-DfsnRoot', [System.Management.Automation.CommandTypes]::Function)
            
            $SkipAccessErrors1 = $SkipAccessErrors
            $IncludeSMBShares1 = $IncludeSMBShares

            $null = $PSBoundParameters.Remove('SkipAccessErrors') 
            $null = $PSBoundParameters.Remove('IncludeSMBShares') 
                        
            if ($IncludeSMBShares1)
            {
                $scriptCmd = {& $wrappedCmd @PSBoundParameters |
                                % { $_ } -PipelineVariable pvDfsnRoot |
	                            % { Get-DfsnFolder -Path $($_.Path + "\*") } |
	                            % { Get-DfsnFolderTarget -Path $_.Path } | Select-Object Path,TargetPath -PipelineVariable a1 |
	                            % { try { Get-SmbShare -CimSession $_.TargetPath.Split('\')[2] -Name $_.TargetPath.Split('\')[3] -ErrorAction SilentlyContinue | Select Name,Path,PSComputerName } 
                                    catch {
                                            if ($SkipAccessErrors1)
                                                { [pscustomobject]@{Name="";Path="";PSComputerName=""} }
                                            else
                                                { [pscustomobject]@{Name="";Path="Access Error";PSComputerName=$($_.Exception.Message)} }
                                          } 
                                   } |
	                            % {Add-Member -InputObject $a1 @{NameSpace=$pvDfsnRoot.Path;ShareLocalPath=$_.Path;ShareName=$_.Name;ShareServer=$_.PSComputerName} -PassThru  }
                              }
            } else {

                $scriptCmd = {& $wrappedCmd @PSBoundParameters |
                                % { $_ } -PipelineVariable pvDfsnRoot |
	                            % { Get-DfsnFolder -Path $($_.Path + "\*") } |
	                            % { Get-DfsnFolderTarget -Path $_.Path } | Select-Object Path,TargetPath 
                             }
            }

            $steppablePipeline = $scriptCmd.GetSteppablePipeline($myInvocation.CommandOrigin)
            $steppablePipeline.Begin($PSCmdlet)

        } catch {
            throw
        }
    }

    process
    {
        try {
#            $steppablePipeline.Process($_)
        } catch {
            throw
        }
    }

    end
    {
        try {
            $steppablePipeline.End()
        } catch {
            throw
        }
    }
    <#

    .ForwardHelpTargetName Get-DfsnRoot
    .ForwardHelpCategory Function

    #>
}

#List DFS Namespaces as Get-DfsnRoot
List-Dfsn

