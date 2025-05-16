
$path = (Get-Location).Path

$files = Get-ChildItem -Path $path -Filter *.py -File
Write-Output "Running mypy on files"
Write-Output $path 
foreach($f in $files){
 Write-Output $f.Name
 mypy $f
}