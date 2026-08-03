import requests
import zipfile
import shutil
import tempfile
from datetime import datetime
import os
import json

webhook_url = "Your_webhook_here"

def report_failure(txt, txt_split, filename):
    zip_name = filesend(txt, txt_split, filename)
    
    with open(zip_name, 'rb') as f:
        data = {"payload_json": json.dumps({"content": "The gym rat counter is down!", "username": "status_bot"})}
        files = {'file': (zip_name, f, 'application/zip')}
        
        response = requests.post(webhook_url, data=data, files=files)
        print(f"Status: {response.status_code}")


def filesend(txt, txt_split, filename):
    temp_dir = tempfile.mkdtemp()
    print(f"Created temp dir {temp_dir}")
    source_file = "logs.csv"
    shutil.copy(source_file, temp_dir)
    print(f"Copied {source_file} to {temp_dir}")
    
    with open(os.path.join(temp_dir, "full_text.txt"), 'w') as file:
        json.dump(txt, file)
        
    with open(os.path.join(temp_dir, "split_text.txt"), 'w') as file:
        json.dump(txt_split, file)
        
    print(f"Created full_text.txt and split_text.txt")
    
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M")
    zip_name = f"{current_time}_logs.zip"
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, arcname=file)
                
    print(f"Archived to {zip_name}")
    shutil.rmtree(temp_dir)
    return zip_name

def report_success():
    with open("logs.csv", "rb") as f:
        payload = {"content":f"Successfully logged {datetime.now().strftime("%Y-%m-%d_%H-%M")}", "username": "status_bot"}
        response = requests.post(webhook_url, data=payload, files={"files":f})
        return response.status_code

if __name__ == "__main__":
    txt, txt_split, filename = "", "", ""
    report_failure(txt, txt_split, filename)