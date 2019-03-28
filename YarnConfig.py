# -*- coding: utf-8 -*-
import ConfigParser
import os
import YarnLog
import logging


filepath = os.getcwd() + os.path.sep + "config"
filename = "ipconfig.ini"
path = filepath + os.path.sep + filename

def getConfig(model,key):
    # read

    if not os.path.isfile(path):
        message = 'Sorry,the config file ["%s"] not exists'
        # print (message % filename)
        logging.warning(message % filename)
    try:
        config = ConfigParser.ConfigParser()
        config.read(path)
        config.write(open(path, "w"))
        if config.has_option(model,key):
            value = config.get(model, key)
            return value
        else:
            logging.debug('Sorry,the key: [ %s ] not exists' % key)
            return 'Nono'
    except ConfigParser.DuplicateSectionError:
        message = 'Sorry,the key: ["%s"] not exists, Plase check the key' % key
        # print(message)
        logging.warning(message)


def setConfig(model,key,value):
    #write
    if not os.path.exists(filepath):
        YarnLog.mkdir(filepath)
    try:
        config = ConfigParser.ConfigParser()
        config.read(path)
        config.add_section(model)
        config.set(model,key,value)
        config.write(open(path, "w"))
    except ConfigParser.DuplicateSectionError:
        print("already exists")

if __name__ == '__main__':
    # setConfig('HOST','host','10.240.2.81')
    host = getConfig('HOST','ip')
    print (host)
