# -*- coding: utf8 -*-
'''
dump data from mysql/hive to load into mysql
'''
from datetime import datetime,timedelta
from optparse import OptionParser
import argparse
import ConfigParser
import sys
import os
import time
import commonutil

def getConf(cfgfile):
    config = ConfigParser.ConfigParser()
    with open(cfgfile, 'r') as cfgfile:
        config.readfp(cfgfile)
    return config

def readFile(fileName):
    infile = open(fileName, "r")
    content = infile.read()
    infile.close()
    return content

def truncateFile(fileName):
    fileTemp = open(fileName, "w")
    fileTemp.truncate()
    fileTemp.close()

def getConnBySecName(dbConf,secName):
    descSec = ''
    secs = dbConf.sections()
    for sec in secs:
        if sec == secName:
            descSec = sec
    conn = getConnOne(dbConf,descSec)
    return conn
    
def getConns(dbConf):
    secs = dbConf.sections()
    conns = {}
    for sec in secs:
        conn = getConnOne(dbConf, sec)
        if conn is not None:
            conns[sec]=conn
    return conns

def getConnOne(dbConf, sec):
    host = dbConf.get(sec,"host")
    port = dbConf.getint(sec,"port")
    user = dbConf.get(sec,"user")
    password = dbConf.get(sec,"password")
    database = dbConf.get(sec,"database")
    conn = commonutil.getConn(host, port, user, password, database)
    if conn is None:
        time.sleep(5)
        conn = commonutil.getConn(host, port, user, password, database)
    if conn is None:
        commonutil.fatal("fail to get connection : sec=[{0}]".format(sec))
    return conn
    
