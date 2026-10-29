$shell = New-Object -ComObject Shell.Application
$folder = $shell.Namespace('c:\Users\bhara\Downloads\GLASNOST-LATEST\website\public\media\audio')
foreach ($item in $folder.Items()) {
    $dur = $folder.GetDetailsOf($item, 27)
    Write-Host "$($item.Name) --> $dur"
}
