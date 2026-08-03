import time
import uiautomator2 as u2
from datetime import datetime
from PIL import Image
import pytesseract
import os, sys
import csv
from discord import report_failure, report_success

try:
    if len(sys.argv)==2:
        device = f"{os.argv[1]}"
    elif len(sys.argv)==3:
        device = f"{os.argv[1]}:{os.argv[0]}"
    elif len(sys.argv)==1:
        device = "192.168.100.168"
        
except IndexError:
    print("Bad arguments")
    
app = "com.perfectgym.perfectgymgo2.wellfitness"
app_activity = "/com.elpassion.perfectgym.splash.SplashActivity"



def text_processing(txt):
    txt_split = txt.split()
    length = len(txt_split)-1
    ppl_count = 0
    
    for i in range(length):
        if txt_split[i+1] == "people":
            return txt_split[i]

    print("Failure! Reporting...")
    report_failure(txt_split, txt, filename)
    return False


def csv_append(ppl_count, filename):
    with open("logs.csv", "a", newline="") as file:
        headers = ['ppl_count', 'date_time']
        writer = csv.DictWriter(file, fieldnames=headers)
        
        writer.writerow({
            'ppl_count':ppl_count,
            'date_time':filename
        })

def phone_stuff():
    d = u2.connect(device)
    if not d.info.get('screenOn'):
        d.press("power")

        
    
    if not d.app_current()["package"] == app:
        d.app_start(app)
        print("Waiting for app to open")
        time.sleep(5)
    
    d.swipe_ext("down", duration=0.2)
    print("Waiting for data pulling")
    time.sleep(1)
    
    return d


def main():
    d = phone_stuff()
    
    global filename 
    filename = datetime.now().strftime("%Y-%m-%d_%H-%M")
    src_filename = filename + ".png"
    d.screenshot(src_filename)

    text = pytesseract.image_to_string(Image.open(src_filename))
    
    ppl_count = text_processing(text)
    if not ppl_count:
        if os.path.exists(filename+"_logs.zip"):
            os.remove(filename+"_logs.zip")
        os.remove(src_filename)
        d.press("power")
        return "Function Error. See discord for logs."
    
        
    print("Logging results")
    csv_append(ppl_count, filename)
    print("Cleaning up")
    os.remove(src_filename)
    if os.path.exists(filename+"_logs.zip"):
        os.remove(filename+"_logs.zip")
    d.press("power")
    print("Reporting success!")
    report_success()
    print("Done!")
    return 0


if __name__ == "__main__":
    main()
