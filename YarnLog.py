# -*- coding: utf-8 -*-
import logging
import time
import os
import YarnConfig
from logging.handlers import TimedRotatingFileHandler

def writeLog(message):

    logger=logging.getLogger()
    filename="yarn_job_" + time.strftime('%Y-%m-%d',time.localtime(time.time())) + ".log"

    path = os.getcwd() + os.path.sep + 'logs'
    mkdir(path)
    logFile = path + os.path.sep + filename
    handler=logging.FileHandler(logFile)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    # fileLog = TimedRotatingFileHandler(logFile, when="S", interval=10, backupCount=4)
    # fileLog.setLevel(logging.WARNING)
    # fileFmt = logging.Formatter('%(asctime)s - [line:%(lineno)d] - %(levelname)s -- %(message)s')
    # fileLog.setFormatter(fileFmt)
    # logger.addHandler(fileLog)
    # logging.basicConfig(filename=logFile, format='%(asctime)s - %(levelname)s - %(message)s',
    #                     datefmt='%Y-%m-%d %H:%M:%S', level=YarnConfig.getConfig('LOG', 'logging.level'), filemode='w')
    logger.info(message)

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
    #else:
        #print ('folder is exist')

def init_logging():
    LOG_FOLDER = YarnConfig.getConfig('LOG','logging.path')
    LOG_SUFFIX = 'yarn_job_' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'
    mkdir(LOG_FOLDER)
    logPath = LOG_FOLDER + os.path.sep + LOG_SUFFIX
    logging.basicConfig(filename=logPath, format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S', level=YarnConfig.getConfig('LOG','logging.level'), filemode='w')
    logging.debug("Log Started...")

if __name__=='__main__':
    writeLog("hello")
