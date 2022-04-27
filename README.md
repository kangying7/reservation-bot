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

## 4. Set up credentials
Update username and password field in the etc/config.txt file

## 5. Start script
```console
python .\schedule_task.py
```