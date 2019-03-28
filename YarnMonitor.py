#!/home/gaojr/Python-2.7.15 python
# -*- coding: utf_8 -*-
from yarn_api_client import ApplicationMaster, ResourceManager
from collections import defaultdict
import os
import logging
import time
import YarnConfig
import YarnLog


# Resource Manager HOST/PORT
RM_HOST = YarnConfig.getConfig('ResourceManager','host')
RM_HOST_BAK = YarnConfig.getConfig('ResourceManager','host_bak')
RM_PORT = YarnConfig.getConfig('ResourceManager','port')

# Application Master HOST/PORT
AM_HOST = YarnConfig.getConfig('ApplicationMaster','host')
AM_PORT = YarnConfig.getConfig('ApplicationMaster','port')

LOG_TIME = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

# get the latest state of all applicatoins
def update_applicatioins_map(rm=None):
    if rm == None:
        return None

    apps = rm.cluster_applications().data
    appsDict = defaultdict()
    update = False

    for app in apps.get('apps').get('app'):
        update = False
        name = app.get('name')
        if name in appsDict:
            newTime = app.get('startedTime')
            oldTime = appsDict.get(name).get('startedTime')
            if newTime > oldTime and name.startswith('com.bos'):
            # if newTime > oldTime:
                update = True
        else:
            if name.startswith('com.bos'):
                stateIn = app.get('state')
                update = True

        if update == True:
            appsDict[name] = app

    return appsDict

def filter_apps_not_state(appsDict={}, state='RUNNING'):
    filteredAppsDict = defaultdict()
    for key in appsDict.keys():
        appDict = appsDict.get(key)
        if key.startswith('com.bos') and appDict.get('state') != state:
            logging.info('%s -INFO - id: %s - name: %s - state: %s' % (
                time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), appDict.get('id'), key,
                appDict.get('state')))
            filteredAppsDict[key] = appDict

    return filteredAppsDict

def filter_apps_state(appsDict={}, state='RUNNING'):
    filteredAppsDict = defaultdict()
    for key in appsDict.keys():
        appDict = appsDict.get(key)
        if key.startswith('com.bos') and appDict.get('state') == state:
            logging.info('%s -INFO - id: %s - name: %s - state: %s' % (
                time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), appDict.get('id'), key,
                appDict.get('state')))
            filteredAppsDict[key] = appDict

    return filteredAppsDict

def duration_timeout_jobs(appId='', AM=None):
    if AM == None or len(appId) <= 0:
        return None

    timeout = YarnConfig.getConfig('JobDuration', 'timeout')
    falg = False

    for job in AM.application_information(appId):
        jobId = job.get('id')
        duration = handle_duration_time(job.get('duration'))
        logging.info('%s - INFO - application: %s - jobId: %s - duration: %s ms' % (
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), appId, jobId, duration))

        if duration >= int(timeout):
            falg = True
        else:
            falg = False

    return falg

def handle_duration_time(duration=''):
    if duration == None or len(duration) <= 0:
        return None

    rtime = float()
    dtime = duration.split(' ')
    if dtime[1] == 'ms':
        rtime = float(dtime[0])
    elif dtime[1] == 's':
        rtime = float(dtime[0])*1000
    elif dtime[1] == 'min':
        rtime = float(dtime[0])*60*1000
    else:
        rtime
    return rtime

def apps_running_duration(appsDict={}, AM=None):
    runningAppsDict = defaultdict()
    for key in appsDict.keys():
        appId = appsDict.get(key).get('id')
        logging.debug('apps_running_duration appid: %s' % appId)
        if duration_timeout_jobs(appId, AM) == True:
            runningAppsDict[key] = appsDict.get(key)

    return runningAppsDict

def start_spark(appsDisct={}):
    for key in appsDisct.keys():
        name = appsDisct.get(key).get('name')
        id = appsDisct.get(key).get('id')
        if YarnConfig.getConfig('TRANSMONITOR',name) != 'Nono':
            start_shell = YarnConfig.getConfig('TRANSMONITOR',name)
            if os.path.exists(start_shell) == True:
                command = ('sh %s %s' %(start_shell, id))
                execute_cmd(command)
                logging.info('%s - INFO - Start Spark -- name: %s - command: %s' % (
                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), name, command))
            else:
                logging.warning('%s - Warning - [%s] - File does not exist!' % (
                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), start_shell))

def kill_spark(appsDisct={}):
    for key in appsDisct.keys():
        name = appsDisct.get(key).get('name')
        id = appsDisct.get(key).get('id')
        if len(id) > 0:
            # id = 'application_1542781021189_0154'
            kill_cmd = 'yarn application -kill ' + id
            # execute_cmd(kill_cmd)
            logging.info('%s - INFO - Spark: - [%s] killed; -- Command: %s' % (
                time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), name, kill_cmd))
        else:
            logging.warning('%s - Warning - [%s] - does not exist!' % (
                time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), id))

def execute_cmd(cmd='ls'):
    if len(cmd) > 0:
        result = os.popen(cmd)
        # lines = result.readlines()
        # for line in lines:
            # print (line)

# logging init
def init_logging():
    LOG_FOLDER = YarnConfig.getConfig('LOG','logging.path')
    LOG_SUFFIX = 'yarn_job_' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'
    path = os.getcwd() + os.sep + LOG_FOLDER
    prepareFolder(LOG_FOLDER)
    logPath = path + os.sep + LOG_SUFFIX
    loglevel = YarnConfig.getConfig('LOG','logging.level')
    logging.basicConfig(filename=logPath, format='%(asctime)s - %(levelname)s -- %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S', level=loglevel, filemode='w')
    logging.info("############################ Start Logging #################################")

# if output path not existed, mkdir
def prepareFolder(folder):
    if os.path.exists(folder) == False:
        os.mkdir(folder)


def rm_active_standby(active=None, back=None):
    active = ResourceManager(address=RM_HOST, port=RM_PORT)
    back = ResourceManager(address=RM_HOST_BAK, port=RM_PORT)

    activeHaState = active.cluster_information().data.get('clusterInfo').get('haState')
    backHaState = back.cluster_information().data.get('clusterInfo').get('haState')

    # state : ACTIVE, STANDBY
    if activeHaState == 'ACTIVE':
        logging.info("ResourceManager host = "+ active.address + " is active")
        return active
    elif backHaState == 'ACTIVE':
        logging.info("ResourceManager host = "+ back.address + " is active")
        return back
    else:
        logging.warning("No ResourceManager can be usered, Please check again")

def main():
    YarnLog.writeLog('init logging')
    # init_logging()

    # RM = rm_active_standby()
    RM = ResourceManager(address=RM_HOST, port=RM_PORT)
    AM = ApplicationMaster(address=AM_HOST, port=AM_PORT)
    appsDict = update_applicatioins_map(RM)

    if YarnConfig.getConfig('MonitorSwitch', 'FinishedSwitch') == 'True':
        logging.info(
            '############################ Filter FINISHED Application and Start it #################################')
        # when spark application finished, start
        # finishedswitch = True
        failedAppsDict = filter_apps_state(appsDict, 'FINISHED')
        start_spark(failedAppsDict)

    if YarnConfig.getConfig('MonitorSwitch', 'FailedSwitch') == 'True':
        logging.info(
            '############################ Filter FAILED Application and Start it #################################')
        # when spark application failed, start
        failedAppsDict = filter_apps_state(appsDict, 'FAILED')
        start_spark(failedAppsDict)

    if YarnConfig.getConfig('MonitorSwitch', 'KilledSwitch') == 'True':
        logging.info(
            '############################ Filter KILLED Application and Start it #################################')

        # when spark application killed by user, start
        killedAppsDict = filter_apps_state(appsDict, 'KILLED')
        start_spark(killedAppsDict)

    if YarnConfig.getConfig('MonitorSwitch', 'RunningSwitch') == 'True':
        logging.info(
            '############################ Filter RUNNING Application and Start it #################################')

        # when spark application is running
        # but the duration time of the current job for more then 2 minute; kill and will be restart by next time
        runningAppsDict = filter_apps_state(appsDict, 'RUNNING')
        durationAppDict = apps_running_duration(runningAppsDict, AM)
        # start_spark(durationAppDict)
        kill_spark(durationAppDict)

    logging.info('############################ Ending ###################################')

if __name__ == '__main__':
    main()
