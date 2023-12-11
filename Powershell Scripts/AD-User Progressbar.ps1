
   ##Nested progress bar

   For ($i=0; $i -le 100; $i++) {
    Start-Sleep -Milliseconds 1
    Write-Progress -Id 1 -Activity "First Write Progress" -Status "Current Count: $i" -PercentComplete $i -CurrentOperation "Counting ..."
 
    For ($j=0; $j -le 100; $j++) {
        Start-Sleep -Milliseconds 1
        Write-Progress -Id 2 -Activity "Second Write Progress" -Status "Current Count: $j" -PercentComplete $j -CurrentOperation "Counting ..."
    }
}

Get-ADUser -Filter * -SearchBase "OU=IT,DC=computacenter,DC=de" `
-Properties Name,GivenName,Surname,Manager