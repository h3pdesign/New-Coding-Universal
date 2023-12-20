Get-ChildItem -Path 'X:\Archive\SSL-Certificates' -Directory | ForEach-Object {
    (Get-ChildItem -Path $_.FullName -Filter 'cert*.pem' -File -Recurse |
    Sort-Object LastWriteTime | Select-Object -Last 1).FullName
}