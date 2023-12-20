Function Get-DateRange {
    <#
    .SYNOPSIS
        Find out all the dates inbetween the range of dates you specify
    .DESCRIPTION
        Simple function to return an array of date/time objects for all days inbetween the two dates
        you specify.
    .PARAMETER Start
        Start date – this specifies the beginning of your range
    .PARAMETER End
        End date – this specifies the ending of your range. This date can be before OR after the Start
        date.
    .INPUTS
        None
    .OUTPUTS
        [DateTime[]]
    .EXAMPLE
        Get-DateRange -Start 7/24/14 -End 7/1/14
        
        Get all of the dates between the 24th to the 1st in reverse order.  24 DateTime objects will
        be returned.
        
    .EXAMPLE
        Get-DateRange -End 8/1/14
        
        Get all of the dates between today and 8/1/14.  As of 7/14/14 that would be 8 dates.
        
    .NOTES
        Author:             h3p
          
        Changelog:
            1.0             Initial Release
    .LINK
        
#>

    [CmdletBinding()]
    Param (
        [datetime]$Start = (Get-Date),
        [datetime]$End = (Get-Date)
    )
    
    ForEach ($Num in (0..((New-TimeSpan –Start $Start –End $End).Days))) {
        $Start.AddDays($Num).Date
    }
}