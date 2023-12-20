Function Get-LetterCount 
{ 
   <# 
   .Synopsis 
    This counts letters in a string  
   .Description 
    This function counts letters in a string 
   .Example 
    Get-LetterCount "this is a string 
    Returns  string length is 16 and copies text to clipboard 
   .Parameter String 
    The input as a string 
   .Notes 
    
 #> 
  Param ([string]$string) 
  Write-Host -ForegroundColor Cyan "string length is" $string.Length 
  $string | clip.exe 
} #end function Get-LetterCount 
 
Set-Alias -Name glc -Value Get-LetterCount