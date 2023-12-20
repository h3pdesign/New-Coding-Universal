Function Rename-Files($path)
{

    Get-ChildItem -path $path | 

    Foreach-Object { 

        if ($_ -is [System.IO.DirectoryInfo]) {

            echo "directory: $_"

            Rename-Files -path $_.FullName

        }
        else {

            $newName = $_.name -replace '[^A-Za-z0-9-_ \.\[\]]', ''

            $newName = $newName -replace ' ', '_'

            if (-not ($_.name -eq $newname)) {

                echo "renaming: $_.Name  to: $newName"

                Rename-Item -Path $_.fullname -newname ($newName) 

            } 

        }

    }

} #end function



Rename-Files -path "C:\path\to\dir\"