# Convert Fahrenheit to Celsius
function ConvertFahrenheitToCelsius([double] $fahrenheit) {
    $celsius = $fahrenheit - 32
    $celsius = $celsius / 1.8
    $celsius
}

$fahrenheit = Read-Host 'Input a temperature in Fahrenheit'
$result = [int](ConvertFahrenheitToCelsius($fahrenheit))
Write-Host "$result Celsius"