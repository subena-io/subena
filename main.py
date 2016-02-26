#!/usr/local/bin/python2.7
# -*-coding:UTF-8-sig -*-

from package.learning.main import execute as executeLearning
from package.alerts.main import execute as calculateAlerts

from base import args

#sudo /usr/local/mysql/support-files/mysql.server start 

if __name__ == '__main__':
    try:
        executeLearning()
        #store alerts
        if args.alerts:
            calculateAlerts()
            
    except Exception as e:
        print e.args;