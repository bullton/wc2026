$file = Get-ChildItem -Path "D:\Code\wc2026" -Filter "*.xlsx" | Where-Object { $_.Name -like "*32*" } | Select-Object -First 1

$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$excel.DisplayAlerts = $false
$wb = $excel.Workbooks.Open($file.FullName)
$ws = $wb.Sheets.Item(1)
$range = $ws.UsedRange

$scenarios = @()

for($i=6; $i -le $range.Rows.Count; $i++) {
    $groups = @()
    for($j=2; $j -le 13; $j++) {
        $val = $ws.Cells.Item($i, $j).Text
        if($val -and $val -ne "-") {
            $groups += $val
        }
    }

    $third_places = @()
    for($j=15; $j -le 22; $j++) {
        $val = $ws.Cells.Item($i, $j).Text
        if($val) {
            $third_places += $val
        }
    }

    $scenario = @{
        "scenario_id" = $i - 5
        "qualifier_groups" = $groups
        "third_places" = $third_places
    }
    $scenarios += $scenario
}

$wb.Close($false)
$excel.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null

Write-Output "Total scenarios: $($scenarios.Count)"
Write-Output ""
Write-Output "Sample scenarios:"
$scenarios[0..4] | ForEach-Object {
    Write-Output "  Scenario $($_.scenario_id): Qualifiers [$($_.qualifier_groups -join ', ')] -> 3rd [$($_.third_places -join ', ')]"
}

$json = $scenarios | ConvertTo-Json -Depth 10
$json | Out-File -FilePath "d:\Code\wc2026\scenarios.json" -Encoding UTF8
Write-Output ""
Write-Output "Saved to scenarios.json"