# ToolAutoMail Installer Script
# Usage: irm https://raw.githubusercontent.com/ThanhTaiDev/ToolAutoMail/main/scripts/install.ps1 | iex

$ErrorActionPreference = "Stop"

# Colors
function Write-Color($text, $color) {
    Write-Host $text -ForegroundColor $color
}

Clear-Host

Write-Color @"

 ████████╗ ██████╗  ██████╗ ██╗         ███╗   ███╗ █████╗ ██╗██╗     
 ╚══██╔══╝██╔═══██╗██╔═══██╗██║         ████╗ ████║██╔══██╗██║██║     
    ██║   ██║   ██║██║   ██║██║         ██╔████╔██║███████║██║██║     
    ██║   ██║   ██║██║   ██║██║         ██║╚██╔╝██║██╔══██║██║██║     
    ██║   ╚██████╔╝╚██████╔╝███████╗    ██║ ╚═╝ ██║██║  ██║██║███████╗
    ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝

"@ Cyan

Write-Color "                    Auto Email Sender Tool Installer" Yellow
Write-Color "                    Author: ThanhTaiDev" Green
Write-Host ""

$installPath = "$env:USERPROFILE\ToolAutoMail"

Write-Color "[*] Installing to: $installPath" Cyan
Write-Host ""

# Create directory
if (Test-Path $installPath) {
    Write-Color "[!] Removing old installation..." Yellow
    Remove-Item -Recurse -Force $installPath
}

New-Item -ItemType Directory -Path $installPath -Force | Out-Null

# Download files
Write-Color "[*] Downloading files from GitHub..." Cyan

$baseUrl = "https://raw.githubusercontent.com/ThanhTaiDev/ToolAutoMail/main"

$files = @(
    "main.py"
)

foreach ($file in $files) {
    Write-Host "    Downloading $file..."
    Invoke-WebRequest -Uri "$baseUrl/$file" -OutFile "$installPath\$file"
}

Write-Host ""
Write-Color "[✓] Installation complete!" Green
Write-Host ""

# Check Python
$pythonPath = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonPath) {
    Write-Color "[!] Python not found! Please install Python first." Red
    Write-Color "    Download: https://www.python.org/downloads/" Yellow
    Write-Host ""
    exit 1
}

Write-Color "[*] Starting Tool..." Cyan
Write-Host ""

# Run
Set-Location $installPath
python main.py

