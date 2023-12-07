# ***Image Producer***
Using to generate and process image
## ***General Information***
### Supporting Features
1. Auto detect faces, resize, rotate, crop and convert image
2. Collage images and template
3. Placing text on manipulated image
4. Generate QR code base on image data
5. Support Windows and Unix

### Future Features
1. Integrate with storage tools like Ownloud, Drive, GGPhoto, Flickr...
2. Auto crawling required images, icon, emoticons
### Prerequisites
- Python >= 3.8
- CV2 (Opencv-python) <= 9.5.0
- Numpy
- PIL (Pillow)
- QRCode

## ***Structure***
Directory structure is shown below:

```
badge_generator/
.
|-- Haar\ Cascade
|   `-- haarcascade_frontalface_default.xml
|-- README.md                -> Should read first
|-- config.ini
|-- config_base.ini          -> Base config for the GUI
|-- crawl_image.py           -> Use for crawling images from HR tool
|-- execute.py               -> Main CLI app
|-- execute_gui.py           -> Main GUI app
|-- fonts
|   |-- ARIALN.TTF
|   |-- ...
|-- img                      -> Your images here
|   |-- cv_img               -> User for image convertion (optional)
|   |   `-- README.md
|   |-- des_img              -> Output here
|   |   `-- README.md
|   |-- src_img              -> Input here
|   |   `-- README.md
|   |-- template             -> Base template
|   |   `-- README.md
|   |   `-- template.png
|   `-- tmp_img              -> User for debug face detection
|       `-- README.md
|-- pictool.conf             -> Root config
|-- pictool.log              -> Root log
|-- requirements.txt
|-- positions.json           -> Positions register
|-- run.bat
|-- run.pyw                  -> Executor
`-- test_gui                 -> For Owncloud feature support
    |-- config_base.ini
    `-- owncloud.py

```
## ***Preparation***
> [Badge Generator](https://github.com/vicdang/badge_generator.git)
```
# Install python
 - Install python >= 3.8

# clone repo
$ git clone https://github.com/vicdang/badge_generator.git
$ cd badge_generator
 
# create virtual envirnoment and activate it
$ python -m venv --prompt badge_gernator .venv
$ source .venv/Scripts/activate

# install python requirements
$ pip install -r requirements.txt
```
## ***Procedure***
1. Design your template and place it in `badge_generator/img/template/` follow format [Template](img/template/README.md)
> - Eg: template.png
2. Place your images in `badge_generator/img/src_img/` follow format [src_img](img/src_img/README.md)
3. Execute commands
4. Get output in `badge_generator/img/des_img/` follow format [des_img](img/des_img/README.md)
---
## ***Execute Command Line***
```
# For quick start
Execute "run.pyw" (doubeclick or run by cmd)

# For quick start with GUI
$ python execute_gui.py

Optional : 
 - Modify configuration
 - click save for the next execution
 - And/Or click execute
```
## ***For General Help***
```
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
```

## ***For Sub Command Help***
```
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

---
# ***Others***
## ***Make Some Cheers***
I was not expecting that, but you can send a beer via 
> PayPal: [@vicdane](https://paypal.me/vicdane)
## Can I request for a feature or support
Reach me out on my mail (git log is your friend), and we can discuss.
