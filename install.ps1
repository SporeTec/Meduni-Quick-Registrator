[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

Invoke-Command {reg import .\regfix.reg *>&1 | Out-Null}
if (-Not (Test-Path -Path '.\python-install.exe')) {
    Invoke-WebRequest "https://www.python.org/ftp/python/3.7.4/python-3.7.4.exe" -OutFile ".\python-install.exe"
}
Invoke-Command {.\python-install.exe /quiet InstallAllUsers=1 PrependPath=1}
Invoke-Command {pip install selenium}
Invoke-Command {cmd.exe /C start https://chromedriver.chromium.org/downloads}