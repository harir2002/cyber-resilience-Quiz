@echo off
echo Initializing Git...
git init
echo.
echo Adding files...
git add .
echo.
echo Committing files...
git commit -m "Complete Cyber Resilience App with Scorecard"
echo.
echo Renaming branch...
git branch -M main
echo.
echo Adding remote...
git remote remove origin 2>nul
git remote add origin https://github.com/harir2002/cyber-resilience-Quiz.git
echo.
echo DONE! Now run: git push -u origin main
