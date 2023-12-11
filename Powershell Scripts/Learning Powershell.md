# Learning Powershell

## Installing PowerShell

First you need to set up your computer working environment if you have not done so.
Choose the platform below and follow the instructions.
At the end of this exercise, you should be able to launch the PowerShell session.

- Get PowerShell by installing package

- [PowerShell on Linux][inst-linux]
- [PowerShell on macOS][inst-macos]
- [PowerShell on Windows][inst-win]

  For this tutorial, you do not need to install PowerShell if you are running on Windows.
  You can launch PowerShell console by pressing Windows key, typing PowerShell, and clicking on Windows PowerShell.
  However if you want to try out the latest PowerShell, follow the [PowerShell on Windows][inst-win].

- Alternatively you can get the PowerShell by [building it](../../README.md#building-powershell)

[inst-linux]: https://docs.microsoft.com/powershell/scripting/setup/installing-powershell-core-on-linux?view=powershell-6
[inst-win]: https://docs.microsoft.com/powershell/scripting/setup/installing-powershell-core-on-windows?view=powershell-6
[inst-macos]: https://docs.microsoft.com/powershell/scripting/setup/installing-powershell-core-on-macos?view=powershell-6

## Getting Started with PowerShell

PowerShell commands follow a Verb-Noun semantic with a set of parameters.
It's easy to learn and use PowerShell.
For example, `Get-Process` will display all the running processes on your system.
Let's walk through with a few examples from the [PowerShell Beginner's Guide](powershell-beginners-guide.md).

Now you have learned the basics of PowerShell.
Please continue reading if you want to do some development work in PowerShell.

### PowerShell Editor

In this section, you will create a PowerShell script using a text editor.
You can use your favorite editor to write scripts.
We use Visual Studio Code (VS Code) which works on Windows, Linux, and macOS.
Click on the following link to create your first PowerShell script.

- [Using Visual Studio Code (VS Code)](https://docs.microsoft.com/powershell/scripting/components/vscode/using-vscode?view=powershell-6)

### PowerShell Debugger

Debugging can help you find bugs and fix problems in your PowerShell scripts.
Click on the link below to learn more about debugging:

- [Using Visual Studio Code (VS Code)](https://docs.microsoft.com/powershell/scripting/components/vscode/using-vscode?view=powershell-6#debugging-with-visual-studio-code)
- [PowerShell Command-line Debugging][cli-debugging]

[use-vscode-editor]:./using-vscode.md#editing-with-vs-code
[cli-debugging]:./debugging-from-commandline.md
[get-powershell]:../../README.md#get-powershell
[build-powershell]:../../README.md#building-the-repository

### PowerShell Testing

We recommend using Pester testing tool which is initiated by the PowerShell Community for writing test cases.
To use the tool please read [Pester Guides](https://github.com/pester/Pester) and [Writing Pester Tests Guidelines](https://github.com/PowerShell/PowerShell/blob/master/docs/testing-guidelines/WritingPesterTests.md).

### Map Book for Experienced Bash users

The table below lists the usage of some basic commands to help you get started on PowerShell faster.
Note that all bash commands should continue working on PowerShell session.

| Bash                            | PowerShell                              | Description
|:--------------------------------|:----------------------------------------|:---------------------
| ls                              | dir, Get-ChildItem                      | List files and folders
| tree                            | dir -Recurse, Get-ChildItem -Recurse    | List all files and folders
| cd                              | cd, Set-Location                        | Change directory
| pwd                             | pwd, $pwd, Get-Location                 | Show working directory
| clear, Ctrl+L, reset            | cls, clear                              | Clear screen
| mkdir                           | New-Item -ItemType Directory            | Create a new folder
| touch test.txt                  | New-Item -Path test.txt                 | Create a new empty file
| cat test1.txt test2.txt         | Get-Content test1.txt, test2.txt        | Display files contents
| cp ./source.txt ./dest/dest.txt | Copy-Item source.txt dest/dest.txt      | Copy a file
| cp -r ./source ./dest           | Copy-Item ./source ./dest -Recurse      | Recursively copy from one folder to another
| mv ./source.txt ./dest/dest.txt | Move-Item ./source.txt ./dest/dest.txt  | Move a file to other folder
| rm test.txt                     | Remove-Item test.txt                    | Delete a file
| rm -r &lt;folderName>           | Remove-Item &lt;folderName> -Recurse    | Delete a folder
| find -name build*               | Get-ChildItem build* -Recurse           | Find a file or folder starting with 'build'
| grep -Rin "sometext" --include="*.cs" |Get-ChildItem -Recurse -Filter *.cs <br> \| Select-String -Pattern "sometext" | Recursively case-insensitive search for text in files
| curl https://github.com         | Invoke-RestMethod https://github.com    | Transfer data to or from the web

### Recommended Training and Reading

- Microsoft Virtual Academy: [Getting Started with PowerShell][getstarted-with-powershell]
- [Why Learn PowerShell][why-learn-powershell] by Ed Wilson
- PowerShell Web Docs: [Basic cookbooks][basic-cookbooks]
- [PowerShell eBook][ebook-from-powershell.com] from PowerShell.com
- [PowerShell-related Videos][channel9-learn-powershell] on Channel 9
- [Learn PowerShell Video Library][powershell.com-learn-powershell] from PowerShell.com
- [PowerShell Quick Reference Guides][quick-reference] by PowerShellMagazine.com
- [PowerShell 5 How-To Videos][script-guy-how-to] by Ed Wilson
- [PowerShell Documentation](https://docs.microsoft.com/powershell)

-----------------------------------------------------------

## How to Create and Run PowerShell Scripts

You can combine a series of commands in a text file and save it with the file extension '.ps1', and the file will become a PowerShell script.
This would begin by opening your favorite text editor and pasting in the following example.

```powershell
# Script to return current IPv4 addresses on a Linux or MacOS host
$ipInfo = ipconfig | Select-String 'inet'
$ipInfo = [regex]::matches($ipInfo,"addr:\b(?:\d{1,3}\.){3}\d{1,3}\b") | ForEach-Object value
foreach ($ip in $ipInfo)
{
    $ip.Replace('addr:','')
}
```

Then save the file to something memorable, such as .\NetIP.ps1.
In the future when you need to get the IP addresses for the node, you can simplify this task by executing the script.

```powershell
.\NetIP.ps1
10.0.0.1
127.0.0.1
```

You can accomplish this same task on Windows.

```powershell
# One line script to return current IPv4 addresses on a Windows host
Get-NetIPAddress | Where-Object {$_.AddressFamily -eq 'IPv4'} | ForEach-Object IPAddress
```

As before, save the file as .\NetIP.ps1 and execute within a PowerShell environment.
Note: If you are using Windows, make sure you set the PowerShell's execution policy to "RemoteSigned" in this case.
See [Running PowerShell Scripts Is as Easy as 1-2-3][run-ps] for more details.

```powershell
NetIP.ps1
127.0.0.1
10.0.0.1
```

## Creating a script that can accomplish the same task on multiple operating systems

If you would like to author one script that will return the IP address across Linux, MacOS, or Windows, you could accomplish this using an IF statement.

```powershell
# Script to return current IPv4 addresses for Linux, MacOS, or Windows
$IP = if ($IsLinux -or $IsMacOS)
{
    $ipInfo = ifconfig | Select-String 'inet'
    $ipInfo = [regex]::matches($ipInfo,"addr:\b(?:\d{1,3}\.){3}\d{1,3}\b") | ForEach-Object value
    foreach ($ip in $ipInfo) {
        $ip.Replace('addr:','')
    }
}
else
{
    Get-NetIPAddress | Where-Object {$_.AddressFamily -eq 'IPv4'} | ForEach-Object IPAddress
}

# Remove loopback address from output regardless of platform
$IP | Where-Object {$_ -ne '127.0.0.1'}
```

[run-ps]:https://www.itprotoday.com/powershell/running-powershell-scripts-easy-1-2-3

-----------------------------------------------------------

## Debugging in PowerShell Command-line

As we know, we can debug PowerShell code via GUI tools like [Visual Studio Code](https://docs.microsoft.com/en-us/powershell/scripting/components/vscode/using-vscode?view=powershell-6#debugging-with-visual-studio-code). In addition, we can
directly perform debugging within the PowerShell command-line session by using the PowerShell debugger cmdlets. This document demonstrates how to use the cmdlets for the PowerShell command-line debugging. We will cover the following topics:
setting a debug breakpoint on a line of code and on a variable.

Let's use the following code snippet as our sample script.

```powershell
# Convert Fahrenheit to Celsius
function ConvertFahrenheitToCelsius([double] $fahrenheit)
{
$celsius = $fahrenheit - 32
$celsius = $celsius / 1.8
$celsius
}

$fahrenheit = Read-Host 'Input a temperature in Fahrenheit'
$result =[int](ConvertFahrenheitToCelsius($fahrenheit))
Write-Host "$result Celsius"
```

 1. **Setting a Breakpoint on a Line**

- Open a [PowerShell editor](README.md#powershell-editor)
- Save the above code snippet to a file. For example, "test.ps1"
- Go to your command-line PowerShell
- Clear existing breakpoints if any

 PS /home/jen/debug>Get-PSBreakpoint | Remove-PSBreakpoint

- Use **Set-PSBreakpoint** cmdlet to set a debug breakpoint. In this case, we will set it to line 5

```powershell
PS /home/jen/debug>Set-PSBreakpoint -Line 5 -Script ./test.ps1

ID Script             Line       Command          Variable          Action
-- ------             ----       -------          --------          ------
 0 test.ps1              5
```

- Run the script "test.ps1". As we have set a breakpoint, it is expected the program will break into the debugger at the line 5.

```powershell

PS /home/jen/debug> ./test.ps1
Input a temperature in Fahrenheit: 80
Hit Line breakpoint on '/home/jen/debug/test.ps1:5'

At /home/jen/debug/test.ps1:5 char:1
+ $celsius = $celsius / 1.8
+ ~~~~~~~~~~~~~~~~~~~~~~~~~
[DBG]: PS /home/jen/debug>>
```

- The PowerShell prompt now has the prefix **[DBG]:** as you may have noticed. This means
 we have entered into the debug mode. To watch the variables like $celsius, simply type **$celsius** as below.
- To exit from the debugging, type **q**
- To get help for the debugging commands, simply type **?**. The following is an example of debugging output.

```PowerShell
[DBG]: PS /home/jen/debug>> $celsius
48
[DBG]: PS /home/jen/debug>> $fahrenheit
80
[DBG]: PS /home/jen/debug>> ?

 s, stepInto         Single step (step into functions, scripts, etc.)
 v, stepOver         Step to next statement (step over functions, scripts, etc.)
 o, stepOut          Step out of the current function, script, etc.

 c, continue         Continue operation
 q, quit             Stop operation and exit the debugger
 d, detach           Continue operation and detach the debugger.

 k, Get-PSCallStack  Display call stack

 l, list             List source code for the current script.
                     Use "list" to start from the current line, "list <m>"
                     to start from line <m>, and "list <m> <n>" to list <n>
                     lines starting from line <m>

 <enter>             Repeat last command if it was stepInto, stepOver or list

 ?, h                displays this help message.


For instructions about how to customize your debugger prompt, type "help about_prompt".

[DBG]: PS /home/jen/debug>> s
At PS /home/jen/debug/test.ps1:6 char:1
+ $celsius
+ ~~~~~~~~
[DBG]: PS /home/jen/debug>> $celsius
26.6666666666667
[DBG]: PS /home/jen/debug>> $fahrenheit
80

[DBG]: PS /home/jen/debug>> q
PS /home/jen/debug>

```

1. **Setting a Breakpoint on a Variable**

- Clear existing breakpoints if there are any

```powershell
 PS /home/jen/debug>Get-PSBreakpoint | Remove-PSBreakpoint
 ```

- Use **Set-PSBreakpoint** cmdlet to set a debug breakpoint. In this case, we set it to line 5

```powershell

 PS /home/jen/debug>Set-PSBreakpoint -Variable "celsius" -Mode write -Script ./test.ps1

```

- Run the script "test.ps1"

  Once hit the debug breakpoint, we can type **l** to list the source code that debugger is currently executing. As we can see line 3 has an asterisk at the front, meaning that's the line the program is currently executing and broke into the debugger as illustrated below.
- Type **q** to exit from the debugging mode. The following is an example of debugging output.

```powershell
./test.ps1
Input a temperature in Fahrenheit: 80
Hit Variable breakpoint on '/home/jen/debug/test.ps1:$celsius' (Write access)

At /home/jen/debug/test.ps1:3 char:1
+ $celsius = $fahrenheit - 32
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~
[DBG]: PS /home/jen/debug>> l


    1:  function ConvertFahrenheitToCelsius([double] $fahrenheit)
    2:  {
    3:* $celsius = $fahrenheit - 32
    4:  $celsius = $celsius / 1.8
    5:  $celsius
    6:  }
    7:
    8:  $fahrenheit = Read-Host 'Input a temperature in Fahrenheit'
    9:  $result =[int](ConvertFahrenheitToCelsius($fahrenheit))
   10:  Write-Host "$result Celsius"


[DBG]: PS /home/jen/debug>> $celsius
48
[DBG]: PS /home/jen/debug>> v
At /home/jen/debug/test.ps1:4 char:1
+ $celsius = $celsius / 1.8
+ ~~~~~~~~~~~~~~~~~~~~~~~~~
[DBG]: PS /home/jen/debug>> v
Hit Variable breakpoint on '/home/jen/debug/test.ps1:$celsius' (Write access)

At /home/jen/debug/test.ps1:4 char:1
+ $celsius = $celsius / 1.8
+ ~~~~~~~~~~~~~~~~~~~~~~~~~
[DBG]: PS /home/jen/debug>> $celsius
26.6666666666667
[DBG]: PS /home/jen/debug>> q
PS /home/jen/debug>

```

Now you know the basics of the PowerShell debugging from PowerShell command-line. For further learning, read the following articles.

## More Reading

- [about_Debuggers](https://docs.microsoft.com/powershell/module/microsoft.powershell.core/about/about_debuggers?view=powershell-6)
- [PowerShell Debugging](https://blogs.technet.microsoft.com/heyscriptingguy/tag/debugging/)

-----------------------------------------------------------

## PowerShell Beginner’s Guide

If you are new to PowerShell, this document will walk you through a few examples to give you some basic ideas of PowerShell.
We recommend that you open a PowerShell console/session and type along with the instructions in this document to get most out of this exercise.

## Launch PowerShell Console/Session

First you need to launch a PowerShell session by following the [Installing PowerShell Guide](./README.md#installing-powershell).

## Getting Familiar with PowerShell Commands

In this section, you will learn how to

- create a file, delete a file and change file directory
- discover what version of PowerShell you are currently using
- exit a PowerShell session
- get help if you needed
- find syntax of PowerShell cmdlets
- and more

As mentioned above, PowerShell commands are designed to have Verb-Noun structure, for instance `Get-Process`, `Set-Location`, `Clear-Host`, etc.
Let’s exercise some of the basic PowerShell commands, also known as **cmdlets**.

Please note that we will use the PowerShell prompt sign **PS />** as it appears on Linux in the following examples.
It is shown as `PS C:\>` on  Windows.

1. `Get-Process`: Gets the processes that are running on the local computer or a remote computer.

By default, you will get data back similar to the following:

```powershell
PS /> Get-Process

Handles   NPM(K)    PM(K)     WS(K)     CPU(s)     Id    ProcessName
-------  ------     -----     -----     ------     --    -----------
    -      -          -           1      0.012     12    bash
    -      -          -          21     20.220    449    powershell
    -      -          -          11     61.630   8620    code
    -      -          -          74    403.150   1209    firefox

…
```

Only interested in the instance of Firefox process that is running on your computer?

Try this:

```powershell
PS /> Get-Process -Name firefox

Handles   NPM(K)    PM(K)     WS(K)    CPU(s)     Id   ProcessName
-------  ------     -----     -----    ------     --   -----------
    -      -          -          74   403.150   1209   firefox

```

Want to get back more than one process?
Then just specify process names and separate them with commas.

```powershell
PS /> Get-Process -Name firefox, powershell
Handles   NPM(K)    PM(K)     WS(K)    CPU(s)     Id   ProcessName
-------  ------     -----     -----    ------     --   -----------
    -      -          -          74   403.150   1209   firefox
    -      -          -          21    20.220    449   powershell

```

1. `Clear-Host`: Clears the display in the host program.

```powershell
PS /> Get-Process
PS /> Clear-Host
```

Type too much just for clearing the screen?

Here is how the alias can help.

1. `Get-Alias`: Gets the aliases for the current session.

```powershell
Get-Alias

CommandType     Name
-----------     ----
…

Alias           cd -> Set-Location
Alias           cls -> Clear-Host
Alias           clear -> Clear-Host
Alias           copy -> Copy-Item
Alias           dir -> Get-ChildItem
Alias           gc -> Get-Content
Alias           gmo -> Get-Module
Alias           ri -> Remove-Item
Alias           type -> Get-Content
…
```

As you can see `cls` or `clear` is an alias of `Clear-Host`.

Now try it:

```powershell
PS /> Get-Process
PS /> cls
```

1. `cd -> Set-Location`: Sets the current working location to a specified location.

```powershell
PS /> Set-Location /home
PS /home>
```

1. `dir -> Get-ChildItem`: Gets the items and child items in one or more specified locations.

```powershell
# Get all files under the current directory:
PS /> Get-ChildItem

# Get all files under the current directory as well as its subdirectories:
PS /> cd $home
PS /home/jen> dir -Recurse

# List all files with "txt" file extension.
PS /> cd $home
PS /home/jen> dir –Path *.txt -Recurse
```

*6. `New-Item`: Creates a new item.

```powershell
# An empty file is created if you type the following:
PS /home/jen> New-Item -Path ./test.txt


    Directory: /home/jen


Mode                LastWriteTime         Length  Name
----                -------------         ------  ----
-a----         7/7/2016   7:17 PM              0  test.txt
```

You can use the `-Value` parameter to add some data to your file.

For example, the following command adds the phrase `Hello world!` as a file content to the `test.txt`.

Because the test.txt file exists already, we use `-Force` parameter to replace the existing content.

```powershell
PS /home/jen> New-Item -Path ./test.txt -Value "Hello world!" -Force

    Directory: /home/jen


Mode                LastWriteTime         Length  Name
----                -------------         ------  ----
-a----         7/7/2016   7:19 PM             24  test.txt

```

There are other ways to add some data to a file.

For example, you can use `Set-Content` to set the file contents:

```powershell
PS /home/jen>Set-Content -Path ./test.txt -Value "Hello world again!"
```

Or simply use `>` as below:

```powershell
# create an empty file
"" > test.txt

# set "Hello world!" as content of test.txt file
"Hello world!!!" > test.txt

```

The pound sign `#` above is used for comments in PowerShell.

1. `type -> Get-Content`: Gets the content of the item at the specified location.

```powershell
PS /home/jen> Get-Content -Path ./test.txt
PS /home/jen> type -Path ./test.txt

Hello world again!
```

1. `del -> Remove-Item`: Deletes the specified items.

This cmdlet will delete the file `/home/jen/test.txt`:

```powershell
PS /home/jen> Remove-Item ./test.txt
```

1. `$PSVersionTable`: Displays the version of PowerShell you are currently using.

Type `$PSVersionTable` in your PowerShell session, you will see something like below.
"PSVersion" indicates the PowerShell version that you are using.

```powershell
Name                           Value
----                           -----
PSVersion                      6.0.0-alpha
PSEdition                      Core
PSCompatibleVersions           {1.0, 2.0, 3.0, 4.0...}
BuildVersion                   3.0.0.0
GitCommitId                    v6.0.0-alpha.12
CLRVersion
WSManStackVersion              3.0
PSRemotingProtocolVersion      2.3
SerializationVersion           1.1.0.1

```

1. `Exit`: To exit the PowerShell session, type `exit`.

```powershell
exit
```

## Need Help

The most important command in PowerShell is possibly the `Get-Help`, which allows you to quickly learn PowerShell without having to search around the internet.

The `Get-Help` cmdlet also shows you how PowerShell commands work with examples.

It shows the syntax and other technical information of the `Get-Process` cmdlet.

```powershell
PS /> Get-Help -Name Get-Process
```

It displays the examples how to use the `Get-Process` cmdlet.

```powershell
PS />Get-Help -Name Get-Process -Examples
```

If you use **-Full** parameter, for example, `Get-Help -Name Get-Process -Full`, it will display more technical information.

## Discover Commands Available on Your System

You want to discover what PowerShell cmdlets available on your system? Just run `Get-Command` as below:

```powershell
PS /> Get-Command
```

If you want to know whether a particular cmdlet exists on your system, you can do something like below:

```powershell
PS /> Get-Command Get-Process
```

If you want to know the syntax of `Get-Process` cmdlet, type:

```powershell
PS /> Get-Command Get-Process -Syntax
```

If you want to know how to use the `Get-Process`, type:

```powershell
PS /> Get-Help Get-Process -Example
```

## PowerShell Pipeline `|`

Sometimes when you run Get-ChildItem or "dir", you want to get a list of files and folders in a descending order.
To achieve that, type:

```powershell
PS /home/jen> dir | Sort-Object -Descending
```

Say you want to get the largest file in a directory

```powershell
PS /home/jen> dir | Sort-Object -Property Length -Descending | Select-Object -First 1


    Directory: /home/jen


Mode                LastWriteTime       Length  Name
----                -------------       ------  ----
-a----        5/16/2016   1:15 PM        32972  test.log

```

## How to Create and Run PowerShell scripts

You can use Visual Studio Code or your favorite editor to create a PowerShell script and save it with a `.ps1` file extension.
For more details, see [Create and Run PowerShell Script Guide][create-run-script]

## Recommended Further Training and Reading

- Video: [Get Started with PowerShell][remoting] from Channel9
- [eBooks from PowerShell.org](https://leanpub.com/u/devopscollective)
- [eBooks from PowerShell.com][ebooks-powershell.com]
- [eBooks List][ebook-list] by Martin Schvartzman
- [Tutorial from MVP][tutorial]
- Script Guy blog: [The best way to Learn PowerShell][to-learn]
- [Understanding PowerShell Module][ps-module]
- [How and When to Create PowerShell Module][create-ps-module] by Adam Bertram
- Video: [PowerShell Remoting in Depth][in-depth] from Channel9
- [PowerShell Basics: Remote Management][remote-mgmt] from ITPro
- [Running Remote Commands][remote-commands] from PowerShell Web Docs
- [Samples for PowerShell Scripts][examples]
- [Samples for Writing a PowerShell Script Module][examples-ps-module]
- [Writing a PowerShell module in C#][writing-ps-module]
- [Examples of Cmdlets Code][sample-code]

## Commercial Resources

- [Windows PowerShell in Action][in-action] by Bruce Payette
- [Windows PowerShell Cookbook][cookbook] by Lee Holmes

[in-action]: https://www.amazon.com/Windows-PowerShell-Action-Bruce-Payette/dp/1633430294
[cookbook]: http://shop.oreilly.com/product/9780596801519.do
[ebook-list]: https://martin77s.wordpress.com/2014/05/26/free-powershell-ebooks/
[ebooks-powershell.com]: http://powershell.com/cs/blogs/ebookv2/default.aspx
[tutorial]: https://www.computerperformance.co.uk/powershell/index.htm
[to-learn]:https://blogs.technet.microsoft.com/heyscriptingguy/2015/01/04/weekend-scripter-the-best-ways-to-learn-powershell/
[ps-module]:https://msdn.microsoft.com/library/dd878324%28v=vs.85%29.aspx
[create-ps-module]:https://www.business.com/articles/powershell-modules/
[remoting]:https://channel9.msdn.com/Series/GetStartedPowerShell3/06
[in-depth]: https://channel9.msdn.com/events/MMS/2012/SV-B406
[remote-mgmt]:https://www.itprotoday.com/powershell/powershell-basics-remote-management
[remote-commands]:https://docs.microsoft.com/powershell/scripting/core-powershell/running-remote-commands?view=powershell-6
[examples]:https://examples.oreilly.com/9780596528492/
[examples-ps-module]:https://msdn.microsoft.com/library/dd878340%28v=vs.85%29.aspx
[writing-ps-module]:https://www.powershellmagazine.com/2014/03/18/writing-a-powershell-module-in-c-part-1-the-basics/
[sample-code]:https://msdn.microsoft.com/library/ff602031%28v=vs.85%29.aspx
[create-run-script]:./create-powershell-scripts.md

-----------------------------------------------------------

## Working with PowerShell Objects

When cmdlets are executed in PowerShell, the output is an Object, as opposed to only returning text.
This provides the ability to store information as properties.
As a result, handling large amounts of data and getting only specific properties is a trivial task.

As a simple example, the following function retrieves information about storage Devices on a Linux or MacOS operating system platform.
This is accomplished by parsing the output of an existing command, *parted -l* in administrative context, and creating an object from the raw text by using the *New-Object* cmdlet.

```powershell
function Get-DiskInfo
{
    $disks = sudo parted -l | Select-String "Disk /dev/sd*" -Context 1,0
    $diskinfo = @()
    foreach ($disk in $disks) {
        $diskline1 = $disk.ToString().Split("`n")[0].ToString().Replace('  Model: ','')
        $diskline2 = $disk.ToString().Split("`n")[1].ToString().Replace('> Disk ','')
        $i = New-Object psobject -Property @{'Friendly Name' = $diskline1; Device=$diskline2.Split(': ')[0]; 'Total Size'=$diskline2.Split(':')[1]}
        $diskinfo += $i
    }
    $diskinfo
}
```

Execute the function and store the results as a variable.
Now retrieve the value of the variable.
The results are formatted as a table with the default view.

*Note: in this example, the disks are virtual disks in a Microsoft Azure virtual machine.*

```powershell
PS /home/psuser> $d = Get-DiskInfo
[sudo] password for psuser:
PS /home/psuser> $d

Friendly Name            Total Size Device
-------------            ---------- ------
Msft Virtual Disk (scsi)  31.5GB    /dev/sda
Msft Virtual Disk (scsi)  145GB     /dev/sdb

```

Passing the variable down the pipeline to *Get-Member* reveals available methods and properties.
This is because the value of *$d* is not just text output.
The value is actually an array of .Net objects with methods and properties.
The properties include Device, Friendly Name, and Total Size.

```powershell
PS /home/psuser> $d | Get-Member


   TypeName: System.Management.Automation.PSCustomObject

Name          MemberType   Definition
----          ----------   ----------
Equals        Method       bool Equals(System.Object obj)
GetHashCode   Method       int GetHashCode()
GetType       Method       type GetType()
ToString      Method       string ToString()
Device        NoteProperty string Device=/dev/sda
Friendly Name NoteProperty string Friendly Name=Msft Virtual Disk (scsi)
Total Size    NoteProperty string Total Size= 31.5GB
```

To confirm, we can call the GetType() method interactively from the console.

```powershell
PS /home/psuser> $d.GetType()

IsPublic IsSerial Name                                     BaseType
-------- -------- ----                                     --------
True     True     Object[]                                 System.Array
```

To index in to the array and return only specific objects, use the square brackets.

```powershell
PS /home/psuser> $d[0]

Friendly Name            Total Size Device
-------------            ---------- ------
Msft Virtual Disk (scsi)  31.5GB    /dev/sda

PS /home/psuser> $d[0].GetType()

IsPublic IsSerial Name                                     BaseType
-------- -------- ----                                     --------
True     False    PSCustomObject                           System.Object
```

To return a specific property, the property name can be called interactively from the console.

```powershell
PS /home/psuser> $d.Device
/dev/sda
/dev/sdb
```

To output a view of the information other than default, such as a view with only specific properties selected, pass the value to the *Select-Object* cmdlet.

```powershell
PS /home/psuser> $d | Select-Object Device, 'Total Size'

Device   Total Size
------   ----------
/dev/sda  31.5GB
/dev/sdb  145GB
```

Finally, the example below demonstrates use of the *ForEach-Object* cmdlet to iterate through the array and manipulate the value of a specific property of each object.
In this case the Total Size property, which was given in Gigabytes, is changed to Megabytes.
Alternatively, index in to a position in the array as shown below in the third example.

```powershell
PS /home/psuser> $d | ForEach-Object 'Total Size'
 31.5GB
 145GB

PS /home/psuser> $d | ForEach-Object {$_.'Total Size' / 1MB}
32256
148480

PS /home/psuser> $d[1].'Total Size' / 1MB
148480
```