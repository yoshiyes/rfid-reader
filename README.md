# rfid-reader
UHF tag reader (rfid) with 3 M6E nano sensors

# Prerequisites

* Python 3

Python module:
* python-dotenv
* python-mercuryapi
* termcolor
* flask
* flask_cors

# Installation

## Linux (Debian)

Install Python ..
```
apt install python3 python3-pip unzip patch xsltproc gcc libreadline-dev python-dev python-setuptools
```
Clone project: 
```
git clone https://github.com/yoshiyes/rfid-reader.git
cd rfid-reader
```
Then install the prerequisites :
```
pip install -r requirements.txt
```

User also need right to control USB on /dev/*** :
```
sudo usermod -a -G dialout $USER
```

## Windows :
Download and install the latest Python version: [Python](https://www.python.org/downloads/)

Download PIP : [Get-pip](https://bootstrap.pypa.io/get-pip.py)
Then install pip thought python :
```
python get-pip.py
```
Then install the prerequisites :
```
pip3 install -U termcolor flask flask-cors python-dotenv
```

# Configuration (.env file)

## Reader configuration
Windows and Linux do not use the same name to access the rfid drive.

Linux : 
```
tmr:///dev/ttyUSB0
```

Windows :
```
tmr:///com2
```

The number may vary depending on the number of devices connected. Whether you are on Windows or Linux, you have to do it right
be careful to use the right port.  
COMX or ttyUSBX (X corresponds to the equipment number)

Under Linux it is possible to list the equipment via the command `ls /dev/ | grep ttyUSB`  
On Windows, from the device manager, in the "Ports (COM and LPT)" tab

## Configuration example
```
# Server IP
SERV_IP=192.168.1.20
GAME_SERV_URL=http://192.168.1.30

# Reader power in centidBm MAX 3000
READER_POWER=800

READER_BLUE=tmr:///dev/ttyUSB0
READER_GREEN=tmr:///dev/ttyUSB1
READER_YELLOW=tmr:///dev/ttyUSB2
```

# Run

```
python3 src/main.py
```