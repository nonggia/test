# -*- coding: utf8 -*-
from datetime import datetime,timedelta
import os
import sys

d = os.path.dirname(__file__)
if d != "" :
    os.chdir(d)
    
import MySQLdb

GLOBAL_DEBUG_LEVEL=4

def debug(msg):
    if GLOBAL_DEBUG_LEVEL >= 5:
        print "[DEBUG][{0}] {1}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg)

def info(msg):
    if GLOBAL_DEBUG_LEVEL >= 4:
        print "[INFO][{0}] {1}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg)
    
def warn(msg):
    if GLOBAL_DEBUG_LEVEL >= 3:
        print "[WARN][{0}] {1}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg)
    
def error(msg):
    if GLOBAL_DEBUG_LEVEL >= 2:
        print "[ERROR][{0}] {1}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg)

def fatal(msg):
    if GLOBAL_DEBUG_LEVEL >= 1:
        print "[FATAL][{0}] {1}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg)
        #TODO: send mail
        
def runCmd(cmd, arg=""):
    cmd = "%s %s" % (cmd, arg)
    ret = os.system(cmd)
    if ret==0:
        info("command succeeded : cmd=[%s]" % cmd)
    else:
        error("command failed : cmd=[%s]" % cmd)
    return ret

                
def getConn(host, port, user, password, database):
    try:
        conn = MySQLdb.connect(host=host, port=port, user=user, passwd=password, db=database, charset='utf8')
    except MySQLdb.Error as e:
        error("connect mysql failed : args=[host={0};port={1};user={2};pswd={3};db={4}] error=[{5};{6}]".format(host, port, user, password, database, e.args[0], e.args[1]))
        return None
    return conn

