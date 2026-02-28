<#
.SYNOPSIS
Configure environment variables for Stanza training and testing.

.DESCRIPTION
Sets up directory paths and environment variables required for training and testing
Stanza NLP modules. This script configures paths for Universal Dependencies data,
NER datasets, constituency parsing data, and processed training/evaluation files.

.NOTES
File Name      : config.ps1
Author         : Stanza Development Team
Prerequisite   : PowerShell 3.0 or higher
Version        : 1.0

Before running training/testing scripts, you should:
1. Download UD data and set UDBASE path
2. Download NER data and set NERBASE path  
3. Download constituency data and set CONSTITUENCY_BASE path
4. Configure DATA_ROOT to point to where processed data will be stored
5. Configure WORDVEC_DIR where word embeddings are stored

.EXAMPLE
PS> .\config.ps1

This will set up default data directories relative to the current location.

.EXAMPLE
PS> $env:UDBASE = "C:\data\universal_dependencies"
    .\config.ps1

Configure UD data path before running the script.

.LINK
http://universaldependencies.org/conll18/data.html
https://universaldependencies.org/
https://www.aclweb.org/anthology/W03-0419.pdf

#>

# ==============================================================================
# Universal Dependencies Base Directory
# ==============================================================================
# Set UDBASE to the location of UD data folder
# The data should be in CoNLL-U format
# Download from: http://universaldependencies.org/conll18/data.html
# For details, see: https://universaldependencies.org/
# When rebuilding models based on Universal Dependencies, download the UD data
# to some directory, set UDBASE to that directory, and uncomment this line.
# Alternatively, put UDBASE in your system environment variables or shell profile.

# $env:UDBASE = "C:\path\to\UD"

# ==============================================================================
# Named Entity Recognition Base Directory
# ==============================================================================
# Set NERBASE to the location of NER data folder
# The data should be in BIO format or convertible to that format
# For details, see: https://www.aclweb.org/anthology/W03-0419.pdf (CoNLL-03 NER)
# Other NER datasets are supported in:
#   stanza\utils\datasets\ner\prepare_ner_dataset.py
# If rebuilding NER data, choose a location for the NER directory
# and set NERBASE to that location.

# $env:NERBASE = "C:\path\to\NER"

# ==============================================================================
# Constituency Parsing Base Directory
# ==============================================================================
# Set CONSTITUENCY_BASE to the location of constituency data folder
# The data will be in dataset-specific format
# A conversion script (stanza\utils\datasets\constituency\prepare_con_dataset.py)
# will convert this into PTB style format
# If processing constituency data, choose a location for the CON data
# and set CONSTITUENCY_BASE to that location.

# $env:CONSTITUENCY_BASE = "C:\path\to\CON"

# ==============================================================================
# Data Processing and Training Output Directories
# ==============================================================================
# $DATA_ROOT is the default home for where preparation script outputs will go.
# Training scripts will look for Stanza formatted data in this directory.

$env:DATA_ROOT = ".\data"
$env:TOKENIZE_DATA_DIR = "$env:DATA_ROOT\tokenize"
$env:MWT_DATA_DIR = "$env:DATA_ROOT\mwt"
$env:LEMMA_DATA_DIR = "$env:DATA_ROOT\lemma"
$env:POS_DATA_DIR = "$env:DATA_ROOT\pos"
$env:DEPPARSE_DATA_DIR = "$env:DATA_ROOT\depparse"
$env:ETE_DATA_DIR = "$env:DATA_ROOT\ete"
$env:NER_DATA_DIR = "$env:DATA_ROOT\ner"
$env:CHARLM_DATA_DIR = "$env:DATA_ROOT\charlm"
$env:CONSTITUENCY_DATA_DIR = "$env:DATA_ROOT\constituency"
$env:SENTIMENT_DATA_DIR = "$env:DATA_ROOT\sentiment"

# ==============================================================================
# Word Vector Data Directory
# ==============================================================================
# Set WORDVEC_DIR to store external word vector embeddings
# These are used for initializing word representations in neural models

$env:WORDVEC_DIR = ".\extern_data\wordvec"

# ==============================================================================
# Output Configuration Summary
# ==============================================================================

Write-Host "Stanza Environment Configuration" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""
Write-Host "Data Root Directory:" -ForegroundColor Cyan
Write-Host "  `$env:DATA_ROOT = $env:DATA_ROOT" -ForegroundColor White
Write-Host ""
Write-Host "Processing Directories:" -ForegroundColor Cyan
Write-Host "  Tokenize:       $env:TOKENIZE_DATA_DIR" -ForegroundColor White
Write-Host "  MWT:            $env:MWT_DATA_DIR" -ForegroundColor White
Write-Host "  Lemma:          $env:LEMMA_DATA_DIR" -ForegroundColor White
Write-Host "  POS:            $env:POS_DATA_DIR" -ForegroundColor White
Write-Host "  Depparse:       $env:DEPPARSE_DATA_DIR" -ForegroundColor White
Write-Host "  NER:            $env:NER_DATA_DIR" -ForegroundColor White
Write-Host "  CharLM:         $env:CHARLM_DATA_DIR" -ForegroundColor White
Write-Host "  Constituency:   $env:CONSTITUENCY_DATA_DIR" -ForegroundColor White
Write-Host "  Sentiment:      $env:SENTIMENT_DATA_DIR" -ForegroundColor White
Write-Host ""
Write-Host "Vector Data Directory:" -ForegroundColor Cyan
Write-Host "  `$env:WORDVEC_DIR = $env:WORDVEC_DIR" -ForegroundColor White
Write-Host ""
Write-Host "Optional Base Directories (uncomment to use):" -ForegroundColor Yellow
Write-Host "  `$env:UDBASE" -ForegroundColor Gray
Write-Host "  `$env:NERBASE" -ForegroundColor Gray
Write-Host "  `$env:CONSTITUENCY_BASE" -ForegroundColor Gray
Write-Host ""
Write-Host "Environment configuration complete!" -ForegroundColor Green
