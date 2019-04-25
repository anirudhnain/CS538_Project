import time
from datetime import datetime

def openTimeLogFile(fileName):
    file= open('./log/'+fileName,"w+")
    return file

def logTime(file, msg):
    currTime = time.strftime("%Y-%m-%d-%H-%M-%S")
    dt = datetime.now()
    file.write(currTime + '-' + str(int(dt.microsecond/1000)) + ':' + msg + '\n')

def closeFile(file):
    file.close()