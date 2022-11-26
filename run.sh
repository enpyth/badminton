file=./log/$(date +%s).log

nohup python3 main.py -m test  > ${file} 2>&1 &
