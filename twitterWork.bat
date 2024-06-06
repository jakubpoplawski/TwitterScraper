"%~dp0.venv/Scripts/python.exe" "%~dp0twitterScraper.py"
timeout /t 10
"%~dp0.venv/Scripts/python.exe" "%~dp0twitterEmailSender.py"
timeout /t 10
PAUSE