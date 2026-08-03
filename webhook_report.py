import requests
import zipfile
import shutil
import tempfile
from datetime import datetime
import os
import json

webhook_url = "Your_webhook_here"

def send_webhook(content: str, file: Optional[str] = None) -> int:
    data = {"payload_json": json.dumps({"content":content, "username":"status_bot"})}
    if file and os.path.exists(file):
        with open(file, "rb") as f:  
            files = {"file":(file, file)}
            requests.post(webhook_url, data=data, files=files)

def create_debug_zip(txt: str, txt_split: str, filename: str):
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
    zip_name = shutil.make_archive(f"{current_time}_log", "zip", temp_dir)
                
    print(f"Archived to {zip_name}")
    shutil.rmtree(temp_dir)
    return zip_name



def report_success() -> int:
    return send_webhook("content":f"Successfully logged {datetime.now().strftime("%Y-%m-%d_%H-%M")}", "logs.csv")

def other_error_occured(log_file: str) -> int:
    return send_webhook("Some exception or error occured, check attached logs", log_file)

def ppl_count_not_found(txt: str, txt_split: str, filename: str) -> int:
    zip_name = create_debug_zip(txt, txt_split, filename)
    return send_webhook("The gym rat counter is down!", zip_name)

if __name__ == "__main__":
    txt, txt_split, filename = "", "", ""
    report_failure(txt, txt_split, filename) 