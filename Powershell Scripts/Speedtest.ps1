#Start-UDPServer

function Start-UDPServer {
    [CmdletBinding()]
    param (
        # Parameter help description
        [Parameter(Mandatory = $false)]
        $Port = 10000
    )
    
    # Create a endpoint that represents the remote host from which the data was sent.
    $RemoteComputer = New-Object System.Net.IPEndPoint([System.Net.IPAddress]::Any, 0)
    Write-Host "Server is waiting for connections - $($UdpObject.Client.LocalEndPoint)"
    Write-Host "Stop with CRTL + C"

    # Loop de Loop
    do {
        # Create a UDP listender on Port $Port
        $UdpObject = New-Object System.Net.Sockets.UdpClient($Port)
        # Return the UDP datagram that was sent by the remote host
        $ReceiveBytes = $UdpObject.Receive([ref]$RemoteComputer)
        # Close UDP connection
        $UdpObject.Close()
        # Convert received UDP datagram from Bytes to String
        $ASCIIEncoding = New-Object System.Text.ASCIIEncoding
        [string]$ReturnString = $ASCIIEncoding.GetString($ReceiveBytes)

        # Output information
        [PSCustomObject]@{
            LocalDateTime = $(Get-Date -UFormat "%Y-%m-%d %T")
            SourceIP      = $RemoteComputer.address.ToString()
            SourcePort    = $RemoteComputer.Port.ToString()
            Payload       = $ReturnString
        }
    } while (1)
}

Test-NetConnectionUDP
function Test-NetConnectionUDP {
    [CmdletBinding()]
    param (
        # Desit
        [Parameter(Mandatory = $true)]
        [int32]$Port,

        # Parameter help description
        [Parameter(Mandatory = $true)]
        [string]$ComputerName,

        # Parameter help description
        [Parameter(Mandatory = $false)]
        [int32]$SourcePort = 50000
    )

    begin {
        # Create a UDP client object
        $UdpObject = New-Object system.Net.Sockets.Udpclient($SourcePort)
        # Define connect parameters
        $UdpObject.Connect($ComputerName, $Port)
    }

    process {
        # Convert current time string to byte array
        $ASCIIEncoding = New-Object System.Text.ASCIIEncoding
        $Bytes = $ASCIIEncoding.GetBytes("$(Get-Date -UFormat "%Y-%m-%d %T")")
        # Send data to server
        [void]$UdpObject.Send($Bytes, $Bytes.length)
    }

    end {
        # Cleanup
        $UdpObject.Close()
    }
}