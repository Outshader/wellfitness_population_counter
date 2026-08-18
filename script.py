import time
import uiautomator2 as u2
import uiautomator2.exceptions as u2e
from datetime import datetime
from PIL import Image
import pytesseract
import os
import csv
from webhook_report import ppl_count_not_found, report_success
import argparse
from dotenv import load_dotenv
from check_valid_parameters import check_address
import sys

load_dotenv("vars.env")








    

    
APP = "com.perfectgym.perfectgymgo2.wellfitness"
APP_ACTIVITY = "/com.elpassion.perfectgym.splash.SplashActivity"


def arguments_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', type=str, default="", help='Port number')
    parser.add_argument('--addr', '-a', type=str, default="192.168.100.168", help='Device IP addr')
    parser.add_argument('--skip', '-s', action='store_true', help='Skip webhook usage, both for ALL reports')
    return parser.parse_args()
        

def get_ppl_count(txt, filename, args):
    txt_split = txt.split()
    length = len(txt_split)-1
    
    for i in range(length):
        if txt_split[i+1] == "people":
            return txt_split[i]

    print("Failure! Reporting...")
    
    if args.skip:
        ppl_count_not_found(txt, txt_split, filename)
    
    return None

def csv_append(ppl_count, filename):
    with open("logs.csv", "a", newline="") as file:
        headers = ['ppl_count', 'date_time']
        writer = csv.DictWriter(file, fieldnames=headers)
        
        writer.writerow({
            'ppl_count':ppl_count,
            'date_time':filename
        })
    return 0


def get_device_address(args):
    if check_address() is True:
        ip = os.getenv('device_default_IP_address')
        port = os.getenv('device_default_port')
        return f"{ip}:{port}"
    return f"{args.addr}:{args.port}"    



def connect_device(device):
    for attempt in range(2):
        try:
            d = u2.connect(device)

        except u2e.ConnectError:
            if attempt == 0:
                port = input("u2a will need a port")
                device = f"{device}:{port}"
            else:
                sys.exit("The connection process failed")

    return d


def prepare_phone(d):
    if not d.info.get('screenOn'):
        d.press("power")
        
    if not d.app_current()["package"] == APP or not d.app_wait(APP, 0):
        d.app_stop(APP)
        d.app_start(APP)
        print(f"Waiting for {APP} to open")
        time.sleep(5)
    
    d.swipe_ext("down", duration=0.2)
    print("Waiting for data pulling")
    time.sleep(10)
    
    return d


def main():
    args = arguments_parser()
    address = get_device_address(args).strip(":")
    d = connect_device(address)
    
    prepare_phone(d)
    
    
    base_filename = datetime.now().strftime("%Y-%m-%d_%H-%M")
    
    screenshot_filename = f"{base_filename}.png"
    d.screenshot(screenshot_filename)
    
    text = pytesseract.image_to_string(Image.open(screenshot_filename))
    
    
    
    ppl_count = get_ppl_count(text, base_filename, args)
    if ppl_count == None:
        cleanup(d, base_filename)
        return "Function Error. See discord for logs."
    
        
    print("Logging results")
    csv_append(ppl_count, base_filename)
    print("Cleaning up")
    cleanup(d, base_filename)
    print("Reporting success!")
    if args.skip:
        report_success(ppl_count)
    print("Done!")
    return 0


def cleanup(d, filename):
    os.remove(filename+".png")
    if os.path.exists(filename+"_logs.zip"):
        os.remove(filename+"_logs.zip")
    d.press("power")
    return 0


if __name__ == "__main__":
    main()
