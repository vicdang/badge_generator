# Image Producer
Using to generate and process image
## Prerequisites
- Python >= 3.8
- CV2
- Numpy
- PIL
- QRCode

## Structure
Directory structure is shown below:

```
ImageProducer/
.
|-- Haar\ Cascade
|   `-- haarcascade_frontalface_default.xml
|-- README.md
|-- config.ini
|-- config_base.ini
|-- execute.py
|-- execute_gui.py
|-- fonts
|   |-- ARIALN.TTF
|   |-- ARIALNB.TTF
|   |-- ARIALNBI.TTF
|   |-- ARIALNI.TTF
|   |-- arial.ttf
|   |-- arialbd.ttf
|   |-- arialbi.ttf
|   |-- ariali.ttf
|   |-- ariblk.ttf
|   |-- calibri.ttf
|   |-- calibrib.ttf
|   |-- calibrii.ttf
|   |-- calibril.ttf
|   |-- calibrili.ttf
|   `-- calibriz.ttf
|-- img
|   |-- cv_img
|   |   `-- doc.txt
|   |-- des_img
|   |   `-- info.txt
|   |-- src_img
|   |   `-- doc.txt
|   |-- template
|   |   `-- template.png
|   `-- tmp_img
|       `-- doc.txt
|-- pictool.conf
|-- pictool.log
|-- requirements.ini
|-- run.bat
`-- test_gui
    |-- config_base.ini
    `-- owncloud.py

```
## Steps
### Install python
 - Install python >= 3.8

### Install required packages
 - pip3 install -r requirements.ini

### Execute command
```
# For quick start
Execute "run.pyw" (doubeclick or run by cmd)

# For quick start with GUI
$ python execute_gui.py
```
Optional : 
 - Modify configuration
 - click save for the next execution
 - And/Or click execute
```
# For general help
$ python execute.py --help
usage: execute.py [-h] [-d] [--test] [-v] {exec} ...

- Authors: Vic Dang 
- Skype: traxanh_dl 
- Usage example: + python execute.py -d -v exec

positional arguments:
  {exec}         Subcommand help
    exec         Full Execution

optional arguments:
  -h, --help     show this help message and exit
  -d, --debug
  --test
  -v, --verbose

# For sub command help
$ python execute.py exec --help
usage: execute.py exec [-h] [-c] [--check-path] [-s SRC_PATH] [-f DES_PATH]
                       [-t TEMPLATE] [-q QR_TEXT] [-a] [-l LOOP] [-i INTERVAL]

optional arguments:
  -h, --help            show this help message and exit
  -c, --convert         Convert image to PNG format (default: False)
  --check-path          Check out put (default: False)
  -s SRC_PATH, --src-path SRC_PATH
                        Path of the source folder (default: img/src_img/)
  -f DES_PATH, --des-path DES_PATH
                        Path of the destination folder (default: img/des_img/)
  -t TEMPLATE, --template TEMPLATE
                        Template file name (default:
                        img/template/template_full.png)
  -q QR_TEXT, --qr-text QR_TEXT
                        RQ code text (default: None)
  -a, --auto-size       Auto size for text (default: True)
  -l LOOP, --loop LOOP  Lopping the process (default: False)
  -i INTERVAL, --interval INTERVAL
                        Interval for looping the process (default: 600)

# Default execution
python execute.py exec

# Enable debug level and verbose
python execute.py -d exec
python execute.py -d -v exec
```
