# PyGator
An useful tool for CPU/GPU params tunning.

## Setup:
1. Setup ADB.
    Add line `export PATH:$PATH:"adb_path ..."` to .bashrc
    `source .bashrc`

2. Install python 2.7(ubuntu default have,skip)

3. Install pip
    `sudo apt-get install python-pip python-dev build-essential`


4. Install matplotlib
    `sudo apt-get install libpng-dev`

    In dependency:
    `tar -xvf freetype-2.6.3.tar.bz2`
    `cd freetype-2.6.3`
    `sudo make install`
    `sudo pip install  matplotlib`

5. Install xlsxwriter
    `sudo pip install  xlsxwriter`

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