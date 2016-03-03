# Ledger dashboard

Simple dashboard for the command line accounting tool [ledger][0] written in python3 and Flask.

## Installation

### For Arch:
* Install prerequisites with `pacman -S python python-pip`

* Install packages with `pip install -r requirements.txt`	

* Copy the settings file with `cp ledgerdashboard/settings.template.py ledgerdashboard/settings.py`

* Edit the new file using `nano ledgerdashboard/settings.py`

* Run the server with `python3 runserver.py`

* Open a web browser and navigate to http://localhost:5000

### For Ubuntu/Debian:
* Be sure to have Python3 requirements with: `sudo apt-get install python3 python3-pip`

* Install packages with `sudo pip3 install -r requirements.txt`. 

* Copy the settings file with `cp ledgerdashboard/settings.template.py ledgerdashboard/settings.py`

* Edit the new file using `nano ledgerdashboard/settings.py`

* Run the server with `python3 runserver.py`

* Open a web browser and navigate to http://localhost:5000

[0]:http://ledger-cli.org/

