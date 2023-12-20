function GetFiles
{
    param(
        [Parameter(Position=0)]
        $path = $pwd, 

        [Parameter(ValueFromRemainingArguments=$true)]
        [string[]]$exclude
    )

    foreach ($item in Get-ChildItem $path)
    {
        if ($exclude | Where {$item -like $_}) { continue }

        $item
        if (Test-Path $item.FullName -PathType Container)
        {
            GetFiles $item.FullName $exclude
        }
    }
}