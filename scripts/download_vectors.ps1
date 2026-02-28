<#
.SYNOPSIS
Download pre-trained word vector embeddings for Stanza supported languages.

.DESCRIPTION
Downloads word vector (embedding) files for all 50+ languages supported by Stanza.
This script fetches vectors from multiple sources:
- CoNLL17 shared task vectors from LINDAT
- FastText Wiki vectors from Facebook/Meta
- Armenian vectors from ISPRAS
- Erzya vectors from mokha/semantics

The vectors are extracted to the specified directory and compressed with xz compression
for efficient storage.

.PARAMETER VectorDir
The target directory where word vectors will be stored. This is typically several
gigabytes in size. If not provided, you will be prompted.

.NOTES
File Name      : download_vectors.ps1
Author         : Stanza Development Team
Prerequisite   : PowerShell 7.5 or higher (includes Invoke-WebRequest)
Version        : 1.0
Estimated Size : ~5-10 GB after download and extraction
Estimated Time : 1-2 hours depending on connection speed

Uses PowerShell's native Invoke-WebRequest for downloads (no curl/wget needed).

Downloads from:
- LINDAT CLARIN Repository (CoNLL17 embeddings)
- Facebook/Meta (FastText vectors)
- ISPRAS (Armenian embeddings)
- mokha/semantics (Erzya embeddings)

Multiple languages supported including:
Afrikaans, Armenian, Breton, Buryat, Chinese, Erzya, Faroese, Gothic, 
Kurmanji, Old French, North Sami, Serbian, Upper Sorbian, Welsh, and more.

.EXAMPLE
PS> .\download_vectors.ps1 -VectorDir "C:\stanza_data\wordvec"

Downloads all word vectors to the specified directory.

.EXAMPLE
PS> .\download_vectors.ps1

Interactive mode - you will be prompted to enter the vector directory path.

.LINK
https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-1989
https://fasttext.cc/docs/en/pretrained-vectors.html
https://fasttext.cc/docs/en/crawl-vectors.html
https://github.com/ispras-texterra/word-embeddings-eval-hy
https://github.com/mokha/semantics

#>

param(
    [Parameter(Position = 0, ValueFromPipeline = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$VectorDir = $null
)

# ==============================================================================
# Constants and Configuration
# ==============================================================================

$CONLL17_URL = "https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-1989/word-embeddings-conll17.tar"
$CONLL17_TAR = "word-embeddings-conll17.tar"

$FASTTEXT_BASE_URL = "https://dl.fbaipublicfiles.com/fasttext/vectors-wiki"

# FastText supported languages with their codes
$FASTTEXT_LANGUAGES = @(
    @{ Lang = "Afrikaans"; FtCode = "af"; LocalCode = "af" },
    @{ Lang = "Breton"; FtCode = "br"; LocalCode = "br" },
    @{ Lang = "Buryat"; FtCode = "bxr"; LocalCode = "bxr" },
    @{ Lang = "Chinese"; FtCode = "zh"; LocalCode = "zh" },
    @{ Lang = "Faroese"; FtCode = "fo"; LocalCode = "fo" },
    @{ Lang = "Gothic"; FtCode = "got"; LocalCode = "got" },
    @{ Lang = "Kurmanji"; FtCode = "ku"; LocalCode = "kmr" },
    @{ Lang = "North_Sami"; FtCode = "se"; LocalCode = "sme" },
    @{ Lang = "Serbian"; FtCode = "sr"; LocalCode = "sr" },
    @{ Lang = "Upper_Sorbian"; FtCode = "hsb"; LocalCode = "hsb" }
)

# ==============================================================================
# Functions
# ==============================================================================

function Write-Status {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Green -BackgroundColor Black
}

function Write-Error-Message {
    param([string]$Message)
    Write-Host "ERROR: $Message" -ForegroundColor Red -BackgroundColor Black
}

function Write-Warning-Message {
    param([string]$Message)
    Write-Host "WARNING: $Message" -ForegroundColor Yellow -BackgroundColor Black
}

function Download-File {
    param(
        [string]$Url,
        [string]$OutputPath
    )
    
    try {
        Write-Status "Downloading from: $Url"
        Write-Status "Saving to: $OutputPath"
        
        # Use PowerShell's native Invoke-WebRequest for downloading
        $ProgressPreference = 'SilentlyContinue'  # Suppress progress bar for cleaner output
        
        $webRequest = @{
            Uri             = $Url
            OutFile         = $OutputPath
            UseBasicParsing = $true
            ErrorAction     = 'Stop'
        }
        
        Invoke-WebRequest @webRequest
        
        if (Test-Path $OutputPath) {
            Write-Status "Successfully downloaded to: $OutputPath"
            return $true
        }
        else {
            Write-Error-Message "Download failed: file was not created at $OutputPath"
            return $false
        }
    }
    catch [System.Net.WebException] {
        Write-Error-Message "Network error downloading from $Url : $($_.Exception.Message)"
        return $false
    }
    catch [System.IO.IOException] {
        Write-Error-Message "IO error saving to $OutputPath : $($_.Exception.Message)"
        return $false
    }
    catch {
        Write-Error-Message "Failed to download from $Url : $($_.Exception.Message)"
        return $false
    }
}

function Extract-Tar {
    param(
        [string]$TarFile,
        [string]$DestinationPath
    )
    
    try {
        Write-Status "Extracting $TarFile..."
        tar -xf $TarFile -C $DestinationPath
        return $true
    }
    catch {
        Write-Error-Message "Failed to extract $TarFile"
        return $false
    }
}

function Prepare-FastTextVectors {
    param(
        [string]$Lang,
        [string]$FtCode,
        [string]$LocalCode
    )
    
    $langDir = Join-Path (Get-Location) $Lang
    New-Item -ItemType Directory -Path $langDir -Force | Out-Null
    
    $url = "$FASTTEXT_BASE_URL/wiki.$FtCode.vec"
    $fname = "$LocalCode.vectors"
    $outputFile = Join-Path $langDir $fname
    
    Write-Status "=== Downloading FastText vectors for $Lang..."
    if (-not (Download-File -Url $url -OutputPath $outputFile)) {
        Write-Error-Message "Failed to download FastText vectors for $Lang"
        return
    }
    
    Write-Status "=== Compressing file $fname..."
    try {
        xz -f $outputFile
    }
    catch {
        Write-Warning-Message "xz compression failed for $fname. File may not be compressed."
    }
}

# ==============================================================================
# Main Script
# ==============================================================================

# Check for VectorDir parameter
if ([string]::IsNullOrWhiteSpace($VectorDir)) {
    $VectorDir = Read-Host "Enter the target directory for word vectors"
}

# Validate and create directory
if (-not (Test-Path $VectorDir)) {
    Write-Status "Creating directory: $VectorDir"
    New-Item -ItemType Directory -Path $VectorDir -Force | Out-Null
}

Set-Location $VectorDir

Write-Status ""
Write-Status "Stanza Word Vector Download Script"
Write-Status "===================================="
Write-Status "Target Directory: $VectorDir"
Write-Status ""

# Download and extract CoNLL17 vectors
Write-Status "Downloading CoNLL17 word vectors. This may take 15-30 minutes..."
if (Download-File -Url $CONLL17_URL -OutputPath $CONLL17_TAR) {
    Extract-Tar -TarFile $CONLL17_TAR -DestinationPath (Get-Location)
    
    if (Test-Path $CONLL17_TAR) {
        Write-Status "Cleaning up temporary tar file..."
        Remove-Item $CONLL17_TAR -Force
    }
}
else {
    Write-Error-Message "Failed to download CoNLL17 vectors"
}

Write-Status ""
Write-Status "Preparing FastText vectors for additional languages..."

foreach ($langInfo in $FASTTEXT_LANGUAGES) {
    Prepare-FastTextVectors -Lang $langInfo.Lang -FtCode $langInfo.FtCode -LocalCode $langInfo.LocalCode
}

# Handle Old French as symlink to French
$oldFrenchDir = Join-Path (Get-Location) "Old_French"
if (-not (Test-Path $oldFrenchDir)) {
    New-Item -ItemType Directory -Path $oldFrenchDir -Force | Out-Null
}

$frenchVectors = Join-Path (Get-Location) "French\fr.vectors.xz"
$oldFrenchVectors = Join-Path $oldFrenchDir "fro.vectors.xz"

if (Test-Path $frenchVectors) {
    Write-Status "Creating link for Old French vectors..."
    New-Item -ItemType HardLink -Path $oldFrenchVectors -Target $frenchVectors -Force | Out-Null
}

Write-Status ""
Write-Status "========================================="
Write-Status "Word vector download complete!"
Write-Status "========================================="
Write-Status "All vectors are stored in: $VectorDir"
Write-Status "Total size: ~5-10 GB (varies by language coverage)"
Write-Status ""
Write-Status "Next steps:"
Write-Status "1. Set `$env:WORDVEC_DIR = '$VectorDir'"
Write-Status "2. Run training scripts with the appropriate vector parameters"
Write-Status ""
