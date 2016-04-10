# PyGator
An useful tool for CPU/GPU params tunning.

## Setup:
1. install python 2.7


2. install pip
`sudo apt-get install python-pip python-dev build-essential`


3. install 
`sudo apt-get install libpng-dev`
`tar -xvf freetype-2.6.3.tar.bz2`
`cd freetype-2.6.3`
`sudo make install`


4. install xlsxwriter
    `pip install  xlsxwriter`

## Run:

### USB ADB

1. connect usb
2. run setup_usb.sh config adb wifi connect
3. run game
4. run as ./start.sh
5. finish and close window.

### WIFI ADB

1. connect wifi
2. connect usb
3. run setup_wifi.sh config adb wifi connect
4. plug out usb
5. run game
6. run as ./start.sh
7. finish and close window.