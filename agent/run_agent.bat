@echo off
setlocal

echo Starting SecureLog Agent >> C:\Users\DELL\Python\SecureLog\agent\agent.log

cd /d C:\Users\DELL\Python\SecureLog

"C:\Users\DELL\Python\SecureLog\venv\Scripts\python.exe" -m agent.agent ^
>> C:\Users\DELL\Python\SecureLog\agent\agent.log 2>&1

echo Agent process exited >> C:\Users\DELL\Python\SecureLog\agent\agent.log

endlocal
