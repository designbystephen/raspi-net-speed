import os
import re
import subprocess
import time
from pathlib import Path

home = str(Path.home())
appName = 'raspi-net-speed'
outfile = home + '/local/' + appName + '/reports/speedtest.csv'

response = subprocess.Popen(
    '/usr/local/bin/speedtest-cli --simple',
    shell=True,
    stdout=subprocess.PIPE
).stdout.read().decode('utf-8')

ping = re.findall('Ping:\s(.*?)\s', response, re.MULTILINE)
download = re.findall('Download:\s(.*?)\s', response, re.MULTILINE)
upload = re.findall('Upload:\s(.*?)\s', response, re.MULTILINE)

ping = ping[0].replace(',', '.')
download = download[0].replace(',', '.')
upload = upload[0].replace(',', '.')

try:
    f = open(outfile, 'a+')
    if os.stat(outfile).st_size == 0:
            f.write('Date,Time,Ping (ms),Download (Mbit/s),Upload (Mbit/s)\r\n')
except:
    pass

f.write('{},{},{},{},{}\r\n'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), ping, download, upload))