import os, dotenv

dotenv.load_dotenv()

def check_address():
    
    ip, port = os.getenv("default_address"), os.getenv("default_port") 
    
    for i in ip.split("."):
        try:
            int(i)
        except ValueError:
            return "Invalid default_address"

    try:
        int(port)
    except ValueError:
        return "Invalid default_port"
    
    return True

def check_webhook():
    webhook = os.getenv("webhook_url")
    if not ("https://discordapp.com/api/webhooks/" in webhook):
        return "Invalid webhook_url"