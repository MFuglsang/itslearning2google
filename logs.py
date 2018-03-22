import os
import os.path
import datetime

def check_logfolder():
    logfolder =  os.path.dirname(os.path.abspath(__file__)) + '/logs'
    if os.path.isdir(logfolder) == False:
        os.mkdir(logfolder)

def check_logfile():
    logfile = os.path.dirname(os.path.abspath(__file__)) + '/logs/logfile.txt'
    if os.path.isfile(logfile) == False:
        f = open(logfile, 'w')
        f.close()

def write_log(message, status):
    logfile = os.path.dirname(os.path.abspath(__file__)) + '/logs/logfile.txt'

    logetry = str(datetime.datetime.now()) + ' -  Status: ' +str(status) + ', Message: ' + str(message) + '\n'


    f = open(logfile, 'ab+')
    f.write(logetry)
    f.close()
