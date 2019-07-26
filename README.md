# 一. Setup
## 1. install yarn-api-client 
 > *you mast **install** yarn-api-client when you use this yarn monitor*
 - `python setup.py build`
 - `python setup.py install`

## 2. uninstall yarn-api-client 
> *when you need **uninstall** this yarn-api-client model,use this*
* pip list
* pip uninstall yarn-api-client

## 3. upate yarn-api-client 
> *when you need **update** python model,you need unintall and update*
* update yarn-api-client
* cp yarn-api-client/base.py base.py.bak

## 4. offline intall python model
> *when you need intall other python model,you can do this* 
* pip freeze > yarn.txt
* mkdir yarnpackage
* pip install --no-index --find-links=yarnpackage/ -r yarn.txt 

# 二. Command
> *you should modify the script permissions* 
* `chmod 774 start_prmsbd.sh`


# 三. Crontab
> *configure crontab task*
- `crontab -l`
- `crontab -e`

## 1.start yarn monitor
```
*/1 * * * * ../yarnmonitor/yarn-monitor/command/start_yarn_monitor.sh >> ../yarnmonitor/yarn-monitor/logs/yarn-corntab.log 2>&1 
* * * * * sleep 60; ../yarnmonitor/yarn-monitor/command/start_yarn_monitor.sh
```

## 2.clear yarn monitor log
```
0 4 * * * ../yarn-monitor/command/clear_log_opm.sh >> ../yarn-monitor/logs/yarn-corntab.log 2>&1

0 4 * * * ../yarnmonitor/yarn-monitor/command/clear_log_opm.sh >> ../yarnmonitor/yarn-monitor/logs/yarn-corntab.log 2>&1
```

# 四. Just for test
## 1. start yarn command
`../python /home/transmonitor/yarn-monitor/YarnMonitor.py`

## 2. Application_Master API
```
curl --compressed -H "Accept: application/json" -X GET "http://***:8088/ws/v1/cluster/apps"
curl --compressed -H "Accept: application/json" -X GET "http://***:8088/ws/v1/cluster/apps"
curl --compressed -H "Accept: application/json" -X GET "http://***:8088/proxy/application_1549963435527_0001/ws/v1/mapreduce/info"

curl --compressed -H "Accept: application/json" -X GET "http://***:8088/proxy/application_1535085750394_0017/ws/v1/mapreduce/info"
curl --compressed -H "Accept: application/json" -X GET "http://***:8088/proxy/application_1535085750394_0017/ws/v2/mapreduce/info"

curl --compressed -H "Accept: application/json" -X GET "http://***:8088/proxy/application_1535085750394_0017/ws/v1/mapreduce/jobs/4536"

curl --compressed -H "Accept: application/json" -X GET "http://***:8088/proxy/application_1548125170651_0090/api/v1/applications"
```

