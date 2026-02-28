uv run ruff check . --select E501 2>&1 | Select-String "E501" | ForEach-Object {
    # Parse: "path\file.py:LINE:COL: E501 Line too long (LENGTH > LIMIT)"
    if ($_ -match "E501 Line too long \((\d+)\s*>\s*(\d+)\)") {
        [PSCustomObject]@{
            File = ($_ -split ":")[0]
            Line = ($_ -split ":")[1]
            Length = [int]$matches[1]
            Limit = [int]$matches[2]
            Message = $_
        }
    }
} | Sort-Object Length -Descending | Select-Object -First 20 | Format-Table -AutoSize
