# JARVIS - Desktop Shortcut Creator
# Run this once to create a desktop shortcut for JARVIS

$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "JARVIS.lnk"

$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "D:\Jarvis_AI\JARVIS.bat"
$Shortcut.WorkingDirectory = "D:\Jarvis_AI"
$Shortcut.Description = "JARVIS AI Desktop Assistant"
$Shortcut.WindowStyle = 7
$Shortcut.Save()

Write-Host ""
Write-Host "  JARVIS shortcut created on your Desktop!" -ForegroundColor Cyan
Write-Host "  Double-click JARVIS on your desktop to launch." -ForegroundColor DarkCyan
Write-Host ""
