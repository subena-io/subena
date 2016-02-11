#!/usr/local/bin/python2.7
# -*-coding:UTF-8-sig -*-

from package.alerts.main import execute as calculateAlerts

#sudo /usr/local/mysql/support-files/mysql.server start 

if __name__ == '__main__':
    try:
        calculateAlerts()
    except Exception as e:
        print e.args;