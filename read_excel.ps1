$file = Get-ChildItem -Path "D:\Code\wc2026" -Filter "*.xlsx" | Where-Object { $_.Name -like "*32*" } | Select-Object -First 1

$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$excel.DisplayAlerts = $false
$wb = $excel.Workbooks.Open($file.FullName)

Write-Output "Sheet names: $($wb.Sheets | ForEach-Object { $_.Name } -join ', ')"

$ws = $wb.Sheets.Item(1)
Write-Output "Sheet 1: $($ws.Name)"
$range = $ws.UsedRange
Write-Output "Rows: $($range.Rows.Count), Columns: $($range.Columns.Count)"

for($i=1; $i -le [Math]::Min($range.Rows.Count, 500); $i++) {
    $cells = @()
    for($j=1; $j -le $range.Columns.Count; $j++) {
        $val = $ws.Cells.Item($i, $j).Text
        if([string]::IsNullOrEmpty($val)) { $val = "-" }
        $cells += $val
    }
    $line = "R$i|" + ($cells -join "|")
    Write-Output $line
}

$wb.Close($false)
$excel.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null