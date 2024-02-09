Invoke-WebRequest -Uri "https://update.code.visualstudio.com/latest/win32-x64/stable" -OutFile "VSCodeSetup-x64.exe"
Start-Process -FilePath "./VSCodeSetup-x64.exe" -ArgumentList "/silent" -Wait
