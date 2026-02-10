# Installing using Scoop
scoop bucket add assemblyai https://github.com/assemblyai/scoop-assemblyai.git
scoop install assemblyai

# Or via PowerShell as an administrator
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm https://raw.githubusercontent.com/AssemblyAI/assemblyai-cli/main/install.ps1 | iex
New-Alias -Name assemblyai -Value $Env:Programfiles/AssemblyAI/assemblyai.exe
