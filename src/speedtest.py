import os
import re
import subprocess
import time
from pathlib import Path
from sys import argv
import upload

home = str(Path.home())
appName = 'raspi-speed-test'
outfile = home + '/local/' + appName + '/reports/speedtest.csv'
willUpload = str(argv[0])

def getSpeedTestResults():
    print('[INFO] Attempting Speedtest')

    ping = -1
    download = -1
    upload = -1

    try:
        response = subprocess.Popen(
            '/usr/local/bin/speedtest-cli --simple --timeout 30',
            shell=True,
            stdout=subprocess.PIPE
        )

        results = response.stdout.read().decode('utf-8')

        if int(response.returncode or 0) <= 1:
            print('[SUCCESS] Speedtest successful')
            ping = re.findall('Ping:\s(.*?)\s', results, re.MULTILINE)
            download = re.findall('Download:\s(.*?)\s', results, re.MULTILINE)
            upload = re.findall('Upload:\s(.*?)\s', results, re.MULTILINE)

            ping = ping[0].replace(',', '.')
            download = download[0].replace(',', '.')
            upload = upload[0].replace(',', '.')
        else:
            print('[FAILURE] Speedtest failure')
    except Exception as e:
        print('[FAILURE] Speedtest CLI failure. {}', str(e))
    finally:
        return ping, download, upload

def uploadSpeedTest():
    fileId = upload.sendToGoogleDrive(
        outfile,
        'text/csv',
        {'name': 'speedtest.csv'}
    )

    return fileId

try:
    ping, download, upload = getSpeedTestResults()

    print('[INFO] Writing results to file')

    f = open(outfile, 'a+')
    if os.stat(outfile).st_size == 0:
        f.write('Date,Time,Ping (ms),Download (Mbit/s),Upload (Mbit/s)\r\n')

    f.write('{},{},{},{},{}\r\n'.format(time.strftime('%m/%d/%y') , time.strftime('%H:%M'), ping, download, upload))

    print('[SUCCESS] Report written to file ')
    print('[INFO] Report available @', outfile)
except Exception as e:
    print('[FAILURE] Error writting report results to file. {}', str(e))

if willUpload.lower() == 'true':
    try:
        fileId = uploadSpeedTest()
    except Exception as e:
        print('[FAILURE] Error uploading SpeedTest results. {}', str(e))

