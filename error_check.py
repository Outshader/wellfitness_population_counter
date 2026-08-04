import os
from webhook_report import other_error_occured


log_file = "error_log.txt"

def main():
    with open(log_file, "r") as f:
        for line in f:
            for word in line.split():
                    if word.lower() in ["error", "exception", "critical"]:
                        other_error_occured(log_file)
                        return 0

if __name__ == "__main__":
    main()
                
            