param(
    [string[]]$DataFiles = @("config.json"),
    [string]$Name = "stash-file-protocol",
    [string]$EntryScript = "stash_file_protocol.py"
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $PSCommandPath
$repoRoot = Resolve-Path (Join-Path $scriptDir "..")
Set-Location -Path $repoRoot

$entryPath = Join-Path $repoRoot $EntryScript
if (-not (Test-Path -LiteralPath $entryPath)) {
    throw "Entry script not found: $EntryScript"
}

$pyinstallerArgs = @(
    "--noconfirm",
    "--clean",
    "--onefile",
    "--name", $Name
)

foreach ($file in $DataFiles) {
    $fullPath = Join-Path $repoRoot $file
    if (-not (Test-Path -LiteralPath $fullPath)) {
        throw "Data file not found: $file"
    }

    # Windows PyInstaller uses semicolon separator: SOURCE;DEST
    $pyinstallerArgs += "--add-data"
    $pyinstallerArgs += "$file;."
}

$pyinstallerArgs += $EntryScript

Write-Host "Building $Name from $EntryScript..."
& uv run --with pyinstaller pyinstaller @pyinstallerArgs

Write-Host "Built: dist/$Name.exe"
