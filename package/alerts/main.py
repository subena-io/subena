#!/usr/local/bin/python2.7
# -*-coding:UTF-8-sig -*-

"""
    Module for getting alerts according to learning program
    Learning Algorithm - 2015 - Subena
"""

import package.learning.parameter as learningParameter

def execute():
        
    #calculate alerts according to the last values
    #learningParameter.getProbaForLastMeasures(10)
    learningParameter.getAlertsFromStats()
    