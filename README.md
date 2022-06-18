# Running the script
Note: Assuming you have virtual environment installed with dependencies set up.

## 1. Start terminal
For Windows, start a Command Prompt window by holding Windows Key + R and entering "cmd".

## 2. Navigate to destination folder
Navigate to the folder in which this program is located at.
```console
cd {destination-Folder}/personal-project
```

## 3. Activate the virtual environment
```console
<venv>\Scripts\activate.bat
```
## 4. Configure settings
Configure the settings in the config.txt file:

- Enter credentials 
- Specify when the scheduler should begin running 
- Configure the details for a single run

## 5. Run the script

For running a single run, run the async_subprocess.py script.
```console
python async_subprocess.py
```

For running a scheduled run, run the automate_reservation.py script.
```console
python schedule_task.py  
```

# To run setup of pip dependencies:
## 1. Install python 3.10 version
Refer to https://www.python.org/downloads/release/python-3100/.

## 2. Create new virtual environment and activate   
```console
python3 -m venv <venv>
<venv>\Scripts\activate.bat
```
Refer to https://docs.python.org/3/library/venv.html.

## 3. Install pip dependencies by running requirements file. 
```console
python -m pip install -r requirements.txt
```

## 4. Set up configurations
Update username and password field in the etc/config.txt file

## 5. Start script
```console
python .\schedule_task.py
```

# To build executable using PyInstaller
## 1. Install pyinstaller
```console
pip install -U pyinstaller
```

## 2. Create one-folder executable by running follow command with added data.
```console
pyinstaller .\schedule_task.py --add-data ".\etc\config.txt;.\etc" --add-data ".\automate_reservation.py;." --add-data ".\lib\;.\lib" --add-data ".\async_subprocess.py;."
```
