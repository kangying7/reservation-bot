# Activate virtual environment venv
.\venv\Scripts\Activate

Write-Output "Running configurations based on config.txt file under etc folder..."

# Run async_subprocess.py script
python3 .\schedule_task.py