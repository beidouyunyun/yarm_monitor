#!/bin/bash
find ../yarnmonitor/yarn-monitor/logs/ -mtime +3 -name "yarn_job*.log" -exec rm -rf {} \;
