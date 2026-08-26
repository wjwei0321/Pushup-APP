@echo off
echo [1/3] Adding files to Git...
git add .

echo [2/3] Committing changes...
git commit -m "Auto-update from local"

echo [3/3] Pushing to GitHub...
git push origin main

echo Done! Vercel will automatically start deploying.
pause
