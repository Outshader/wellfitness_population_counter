import os
from webhook_report import other_error_occured


log_file = "error_log.txt"

def main():
    with open(log_file, "r") as f:
        for i in ["error", "exception", "critical"]:
            if i in f:
                ppl_count_not_found(None, None, None, 3)
                return 0

if __name__ == "__main__":
    main()
                
            