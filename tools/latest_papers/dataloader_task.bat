@echo off
REM Navigate to the directory containing your Python script and Git repository
cd C:\Users\Utente\OneDrive - Massachusetts Institute of Technology\BSFS Quant\tools\latest_papers

REM Run the Python script
python dataloader.py

REM Add all changes to Git
git add .

REM Commit the changes with a message
git commit -m "Automated update from dataloader"

REM Push the changes to the remote repository
git push origin main
