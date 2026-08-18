# WARNING
This repo has been depracated, will likley not be updated further. The concept has been moved to an API approach here:
https://github.com/Outshader/wellfitness_statistics_api

~~
## WARNING
This repo isn’t really meant to be used by other people because I didn’t have a motivation to really make it so. If you do want me to make it into actually usable software. Contact me somewhere, like here:
arturn011 on discord or join the discord server if you want to https://discord.gg/a35YBCdyTC. Or you can make a thingy here on github, like an issue, discussion or whatnot.
~~

### Short Description
wellfitness_population_counter uses UIAutomator2 to take a screenshot of the well fitness app and tesseract to get the number of people at the gym. It will put that info into a .csv file and then report success to your webhook.

Or in a case of failure it will report failure zipping used text extracted from the screenshot along with the .csv.

Anyhow, the csv can be eventually used to calculate times when there’s least amount of people present.


## Specific documentation
The program uses UIAutmoator2 for Android-related actions such as scrolling, taking screenshots or opening apps.

The program was primarly made for a XIAOMI device, and so I can’t promise that it will work on other devices too. The docs will also be pointed at XIAOMI phones, if you have a different device just refer to your device’s docs.

  

### Installation

To install just run

`git clone https://github.com/Outshader/wellfitness_population_counter`

Change the parameter webhook_url in webhook_report.py. Optionally you can also change the device parameter in script.py so you don’t have to give the parameters later.

### Prerequisites

**Misc. Python packages** - You can either use the venv that comes with the program or use your own. If you’re using your own run

`pip install -r requirements.txt`

In the cloned directory.

  

**TesseractOCR** - Python package (included in venv and requirements.txt) and a binary installed on your system and added to PATH. Installation steps for the binary can be found here:

https://github.com/tesseract-ocr/tesseract#installing-tesseract

  

**ADB debugging enabled** - for guidance refer to your device’s guidelines for enabling.

  

**USB debugging (Security settings)** - this setting is primarly needed and available on XIAOMI-related devices. To enable it refer to your devices guidelines. Generally you will need a sim card to enable said setting. On Oppo, Realme and OnePlus this setting is usually named **“Disable permission monitoring”**.

  

## Quick start




### Prerequisites
To run this project you will need: 

### Installation

To install most things just run

`git clone https://github.com/Outshader/wellfitness_population_counter`

### Usage

Change variables in vars.env to yours. You can also skip the variables but then you'll have to pass arguments to the script. Arguments are as follows:

--port | -p <device_port> Define device's port to use 

--addr | -a <device_ip> Define device's IP to connect to

If both the .env file and the arguments won't be defined

#### Usage

`script.py [--port | -p] <device_ip> [--addr | -a] <device_port> `


## Roadmap

* [x] autodiscovery of devices

* [ ] statistics reliance improvement by accounting for classes via their site

* [ ] dry runs
