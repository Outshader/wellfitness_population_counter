@echo on
cd /d "<Script's location>"
"<python_binary_location>" script.py > error_log.txt 2>&1
"<python_binary_location>" error_check.py
timeout /t 10