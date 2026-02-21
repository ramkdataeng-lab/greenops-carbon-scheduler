@echo off
echo ========================================================
echo       Upload GreenOps Tool to GitHub
echo ========================================================
echo.
echo 1. I will open the GitHub "Create New Repository" page for you.
echo 2. Please name the repository: greenops-carbon-scheduler
echo 3. Click "Create repository".
echo 4. Copy the HTTPS URL (e.g., https://github.com/username/greenops-carbon-scheduler.git).
echo.
pause
start https://github.com/new
echo.
set /p REPO_URL="Paste the GitHub Repository URL here: "
echo.
echo Adding remote origin...
git remote add origin %REPO_URL%
echo.
echo Pushing code to GitHub...
git branch -M main
git push -u origin main
echo.
echo ========================================================
echo       Done! Your tool is now live on GitHub.
echo ========================================================
pause
