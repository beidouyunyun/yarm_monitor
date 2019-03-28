## Setup
pip list
pip uninstall yarn-api-client

* update yarn-api-client
    cp yarn-api-client/base.py base.py.bak
    update
    
  /home/gaojr/Python-2.7.15/python setup.py build
  /home/gaojr/Python-2.7.15/python setup.py install

* pip freeze > yarn.txt
* mkdir yarnpackage
* pip install download yarnpackage/ -r yarn.txt
* pip install --no-index --find-links=yarnpackage/ -r yarn.txt
* pip install --no-index --find-links=/boslog/superset/impala/ -r /boslog/superset/impala.txt
* pip install --no-index --find-links=/boslog/superset/impala/ -r /boslog/superset/impyla.txt
* pip install --no-index --find-links=/boslog/superset/mysql/ -r /boslog/superset/mysql/mysql.txt

## Command
* chmod 774 start_prmsbd.sh


## Crontab
crontab -l
crontab -e

## start yarn monitor
*/1 * * * * /home/gaojr/yarn-monitor/command/start_yarn_monitor.sh >> /home/gaojr/yarn-monitor/logs/yarn-corntab.log 2>&1
* * * * * sleep 60; /home/gaojr/Python-2.7.15/python YarnMonitor.py >> /home/gaojr/crobtab.log


*/1 * * * * /bigdata/yarnmonitor/yarn-monitor/command/start_yarn_monitor.sh >> /bigdata/yarnmonitor/yarn-monitor/logs/yarn-corntab.log 2>&1
* * * * * sleep 60; /bigdata/yarnmonitor/yarn-monitor/command/start_yarn_monitor.sh

## clear yarn monitor log
0 4 * * * /home/gaojr/yarn-monitor/command/clear_log_opm.sh >> /home/gaojr/yarn-monitor/logs/yarn-corntab.log 2>&1

0 4 * * * /bigdata/yarnmonitor/yarn-monitor/command/clear_log_opm.sh >> /bigdata/yarnmonitor/yarn-monitor/logs/yarn-corntab.log 2>&1

## start yarn command
/home/gaojr/Python-2.7.15/python /home/gaojr/yarn-monitor/YarnMonitor.py

## Application_Master API
curl --compressed -H "Accept: application/json" -X GET "http://zjywdsj01:8088/ws/v1/cluster/apps"
curl --compressed -H "Accept: application/json" -X GET "http://namenodea.bos.opmbd.com:8088/ws/v1/cluster/apps"
curl --compressed -H "Accept: application/json" -X GET "http://namenodea.bos.opmbd.com:8088/proxy/application_1549963435527_0001/ws/v1/mapreduce/info"

curl --compressed -H "Accept: application/json" -X GET "http://datanode1.bos.opmbd.com:8088/proxy/application_1535085750394_0017/ws/v1/mapreduce/info"
curl --compressed -H "Accept: application/json" -X GET "http://datanode1.bos.opmbd.com:8088/proxy/application_1535085750394_0017/ws/v2/mapreduce/info"

curl --compressed -H "Accept: application/json" -X GET "http://datanode1.bos.opmbd.com:8088/proxy/application_1535085750394_0017/ws/v1/mapreduce/jobs/4536"

curl --compressed -H "Accept: application/json" -X GET "http://zjywdsj01:8088/proxy/application_1548125170651_0090/api/v1/applications"

