<#
.SYNOPSIS
Analyze and summarize ruff linting violations by rule code.

.DESCRIPTION
Runs ruff check with all rules (excluding Q and E rules) and generates a summary
showing violation counts grouped by rule code. Results are sorted by count in
descending order, making it easy to identify the most common issues.

.PARAMETER Format
Output format: 'Table' (default), 'List', or 'CSV'

.PARAMETER Top
Number of top rules to display (default: all)

.PARAMETER ExportCsv
Optional CSV file path to export results (e.g., 'ruff-violations.csv')

.EXAMPLE
PS> .\ruff-summary.ps1

Runs analysis and displays results in table format sorted by violation count.

.EXAMPLE
PS> .\ruff-summary.ps1 -Top 10 -Format Table

Show only top 10 rules with the most violations.

.EXAMPLE
PS> .\ruff-summary.ps1 -ExportCsv "violations.csv"

Export summary to CSV file for further analysis.

.NOTES
File Name      : ruff-summary.ps1
Author         : Stanza Development Team
Prerequisite   : PowerShell 7.5+, uv, ruff
Version        : 1.0

Analyzes violations from:
- All rule codes except Q (flake8-quotes) and E (pycodestyle errors)
- Preview rules enabled for additional checks
#>

param(
    [Parameter(Position = 0)]
    [ValidateSet('Table', 'List', 'CSV')]
    [string]$Format = 'Table',
    
    [Parameter(Position = 1)]
    [int]$Top = 0,
    
    [string]$ExportCsv = $null
)

# Color functions for output
function Write-Header {
    param([string]$Message)
    Write-Host "`n$Message" -ForegroundColor Cyan -BackgroundColor Black
    Write-Host ("=" * $Message.Length) -ForegroundColor Cyan
}

function Write-Info {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "WARNING: $Message" -ForegroundColor Yellow
}

# ==============================================================================
# Main Script
# ==============================================================================

Write-Header "Ruff Linting Analysis - All Rules (excluding Q, E)"

Write-Info "Running ruff check with --select ALL --preview --ignore Q,E..."
Write-Host ""

try {
    # Run ruff check and capture output
    $ruffOutput = uv run ruff check . --select ALL --preview --ignore "Q,E" 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Warning "No violations found!"
        exit 0
    }
    
    # Parse output and extract rule codes
    # Format: path/file.py:LINE:COL: RULE_CODE Message
    $violations = @()
    
    foreach ($line in $ruffOutput) {
        # Match pattern: RULE_CODE (e.g., F401, W292, etc.)
        if ($line -match ':\s+([A-Z]\d{3,4})\s') {
            $ruleCode = $matches[1]
            $violations += $ruleCode
        }
    }
    
    if ($violations.Count -eq 0) {
        Write-Warning "No violations matched the filter criteria."
        exit 0
    }
    
    # Group and count violations
    $summary = $violations | 
        Group-Object | 
        Select-Object @{n='Rule';e={$_.Name}}, @{n='Count';e={$_.Count}} |
        Sort-Object Count -Descending
    
    # Apply Top filter if specified
    if ($Top -gt 0) {
        $summary = $summary | Select-Object -First $Top
    }
    
    # Display results
    Write-Header "Violation Summary by Rule"
    
    if ($Format -eq 'Table') {
        $summary | Format-Table -AutoSize -Property @{n='Rule Code';e='Rule';w=12}, @{n='Violations';e='Count';w=12}
    }
    elseif ($Format -eq 'List') {
        $summary | ForEach-Object {
            Write-Host "$($_.Rule) : $($_.Count) violations" -ForegroundColor White
        }
    }
    elseif ($Format -eq 'CSV') {
        $summary | Format-Table -AutoSize -Property Rule, Count
    }
    
    # Display statistics
    Write-Header "Statistics"
    Write-Host "Total Rule Types:  $($summary.Count)"
    Write-Host "Total Violations:  $($summary.Count | ForEach-Object { $_ } | Measure-Object -Sum | Select-Object -ExpandProperty Sum)"
    Write-Host "Most Common Rule:  $($summary[0].Rule) ($($summary[0].Count) violations)"
    Write-Host "Least Common Rule: $($summary[-1].Rule) ($($summary[-1].Count) violations)"
    
    # Export to CSV if requested
    if ($ExportCsv) {
        Write-Info "`nExporting results to: $ExportCsv"
        $summary | Export-Csv -Path $ExportCsv -NoTypeInformation
        Write-Info "Export complete!"
    }
    
    # Display top violations for context
    Write-Header "Top Violations (by frequency)"
    $summary | Select-Object -First 10 | Format-Table -AutoSize
    
    Write-Host ""
    Write-Info "Analysis complete!"
    
}
catch {
    Write-Error "Error running ruff analysis: $($_.Exception.Message)"
    exit 1
}
