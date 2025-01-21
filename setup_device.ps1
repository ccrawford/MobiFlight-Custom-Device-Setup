# Check if arguments are provided
param (
    [Parameter(Mandatory=$true)]
    [string]$DeviceName,

    [Parameter(Mandatory=$true)]
    [string]$Prefix
)

# Clone the repository
Write-Host "Cloning CommunityTemplate repository..."
git clone https://github.com/MobiFlight/CommunityTemplate.git $DeviceName

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to clone repository. Exiting."
    exit 1
}

# Run the Python script
Write-Host "Running MobiflightTemplater..."
python ..\..\scripts\MobiflightTemplater.py .\$DeviceName $DeviceName $Prefix

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to run MobiflightTemplater script. Exiting."
    exit 1
}

# Change directory to the new device folder
Set-Location -Path $DeviceName

# Remove the Git remote origin
Write-Host "Removing Git remote origin..."
git remote remove origin

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to remove Git remote. Exiting."
    exit 1
}

# Open in Visual Studio Code
Write-Host "Opening in Visual Studio Code..."
code .

Write-Host "Setup completed successfully!"
