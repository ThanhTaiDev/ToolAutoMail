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

# Download .exe file
Write-Color "[*] Downloading ToolAutoMail.exe from GitHub..." Cyan
Write-Host ""

# Get latest release
try {
    $releasesUrl = "https://api.github.com/repos/ThanhTaiDev/ToolAutoMail/releases/latest"
    $release = Invoke-RestMethod -Uri $releasesUrl -ErrorAction Stop
    $exeAsset = $release.assets | Where-Object { $_.name -eq "ToolAutoMail.exe" }
    
    if ($exeAsset) {
        $downloadUrl = $exeAsset.browser_download_url
        Write-Host "    Downloading from: $($release.tag_name)"
    } else {
        throw "ToolAutoMail.exe not found in latest release"
    }
} catch {
    Write-Color "[!] Could not fetch latest release, using fallback URL..." Yellow
    # Fallback to a direct URL (you need to update this after creating first release)
    $downloadUrl = "https://github.com/ThanhTaiDev/ToolAutoMail/releases/latest/download/ToolAutoMail.exe"
}

Write-Host "    Downloading ToolAutoMail.exe..."
Invoke-WebRequest -Uri $downloadUrl -OutFile "$installPath\ToolAutoMail.exe" -ErrorAction Stop

Write-Host ""
Write-Color "[✓] Installation complete!" Green
Write-Host ""
Write-Color "[*] Starting Tool..." Cyan
Write-Host ""

# Run .exe
Set-Location $installPath
Start-Process -FilePath ".\ToolAutoMail.exe" -NoNewWindow -Wait

