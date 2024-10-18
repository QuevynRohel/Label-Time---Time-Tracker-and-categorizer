@echo off
powershell -Command "Start-Process powershell -ArgumentList '-NoExit', '-Command', 'Set-Location -Path \"%CD%\"; pip install -r requirements.txt' -Verb RunAs"