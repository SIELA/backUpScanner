# -*- coding: utf-8 -*-
'''

Backup file scanner

use : python ./backUpScanner.py -h www.google.com -t 5
      python ./backUpScanner.py -H TargetFile.txt -t 5

No need for delay and use only one thread for one target
 because only 200+ requests for per target

'''

import signal
import argparse
import requests
import IPy
import threading
import time
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
print("#### Backup files scanner ####")

threadsnum = 3
ctrlcstop = False
verbose = True
delay = 0
targets = []
suffixes = []
file_names = []
out_file = []
suffix_file = './suffixes.txt'
filename_file = './filenames.txt'
file_paths = []

#Cmd args parse
parser = argparse.ArgumentParser(description = 'backUpScanner.')
group = parser.add_mutually_exclusive_group()
group.required = True
group.add_argument('--target', '-T', help = 'Single target')
group.add_argument('--targetsfile', '-M', help = 'Targets file')
parser.add_argument('--threads', '-t', help = 'Set threads num', default = 3)
parser.add_argument('--verbose', '-v', help = 'Set verbose level', default = 1)
parser.add_argument('--delay', '-d', help = 'Set delay time', type = int, default = 0)

args = parser.parse_args(['-M','targets.txt','-v','0','-d','1','-t','5'])
#args = parser.parse_args()

#set threads and delay
threads = args.threads
delay = args.delay

if args.verbose == 0:
    verbose = False
else:
    verbose = True
    
#get targets
if args.target != None:
    out_file = args.target
    targets.append(args.target)
else:
    out_file = args.targetsfile+'.out'
    with open(str(args.targetsfile), 'r') as f:
        for line in f.readlines():
            targets.append(line.strip())

#get suffixes
with open(suffix_file, 'r') as sfxs:
    for sfx in sfxs.readlines():
            suffixes.append(sfx.strip())
            
#get filenames
with open(filename_file, 'r') as fns:
    for fn in fns.readlines():
            file_names.append(fn.strip())

#get common name for scan
def get_common_name(target):
    if target.count('.') >= 2:
        return target.split('.')[-2:-1][0]
    elif target.count('.') == 1:
        return target.split('.')[0]
    else:
        return target
    
#judge if a string is ip addr
def is_ip(address): 
    try: 
        IPy.IP(address) 
        return True
    except Exception as e: 
        return False

#combine addr-filename-suffix to url
def combine_urls():
    for fn in file_names:
        for sfx in suffixes:
            file_paths.append(fn+sfx)
            
#send head request to detect if file exists
def detect(url):
    if verbose != False:
        print("[Scanning]: "+url)
    try:
        time.sleep(delay)
        r = requests.head('http://'+url)
        if r.status_code == 200:
            return url
        else:
            return False
    except Exception as e:
        return False

#get result and save
def get_result(target):
    #use common name check first
    if is_ip(target) != True:
        for sfx in suffixes:
            url = target+'/'+get_common_name(target)+sfx
            rs = detect(url)
            if rs != False:
                out.write(rs)
                print("[Detected]: "+rs)
            
    for fp in file_paths:
        url = target+'/'+fp
        rs = detect(url)
        if rs != False:
            out.write(rs)
            print("[Detected]: "+rs)

out = open(out_file, 'w')

#main
combine_urls()
executor = ThreadPoolExecutor(max_workers=threadsnum)

try:
    #我这是写了个屎，还是找大佬帮忙把
except KeyboardInterrupt as e:
    print("Stop by keyboard.")

print("\nScan end. Result saved to "+out_file)
out.close()


