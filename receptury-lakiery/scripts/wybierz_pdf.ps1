param(
    [string]$StartDir = "",
    [string]$OutFile = ""
)
Add-Type -AssemblyName System.Windows.Forms | Out-Null
[System.Windows.Forms.Application]::EnableVisualStyles()
$d = New-Object System.Windows.Forms.OpenFileDialog
$d.Filter = 'PDF (*.pdf)|*.pdf|Wszystkie pliki (*.*)|*.*'
$d.Title = 'Wskaż PDF receptury Autocolor / Duxone'
$d.Multiselect = $false
$d.CheckFileExists = $true
$d.RestoreDirectory = $true
$d.DefaultExt = 'pdf'
if ($StartDir -and (Test-Path -LiteralPath $StartDir)) {
    $d.InitialDirectory = (Resolve-Path -LiteralPath $StartDir).Path
} elseif (Test-Path 'E:\') {
    $d.InitialDirectory = 'E:\'
} else {
    $d.InitialDirectory = [Environment]::GetFolderPath('MyDocuments')
}
if (-not $OutFile) {
    $OutFile = Join-Path $env:TEMP 'receptury_pdf_wybor.txt'
}
$ok = $d.ShowDialog()
if ($ok -eq [System.Windows.Forms.DialogResult]::OK) {
    [System.IO.File]::WriteAllText($OutFile, $d.FileName, [System.Text.UTF8Encoding]::new($false))
    exit 0
}
[System.IO.File]::WriteAllText($OutFile, '', [System.Text.UTF8Encoding]::new($false))
exit 3
