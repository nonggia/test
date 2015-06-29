# -*- coding: utf8 -*-

import smtplib
from datetime import datetime, timedelta
import time
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
import ConfigParser
from optparse import OptionParser
import argparse
import sys
import os
import reportutil
import commonutil 
import dumpmysql

def getOptions():
    parser = OptionParser()
    parser.add_option("-d", "--date", dest="targetDate", help="target date")
    (options, args) = parser.parse_args()
    return options

def getTargetDate(targetDate):
    if targetDate is None:
        #默认是昨天
        targetDate = datetime.now()+timedelta(days=-1)
        commonutil.info("use default target hour : date=[{0}]".format(targetDate))
    else:
        targetDate = datetime.strptime(targetDate,'%Y-%m-%d')
        commonutil.info("target date : date=[{0}]".format(targetDate))
    return targetDate

def makeTrs(templateFileName, dateFileName):
    content = ""
    template = reportutil.readFile(templateFileName)
    dateFile = open(dateFileName, "r")
    for line in dateFile:
        fields = line.strip("\n").split("\x01")
        #计算某些列
	fields[5] = (int)(fields[4]) - (int)(fields[3])
        fields[6] = (int)(fields[2]) - (int)(fields[5])
        if fields[3] == "0":
            fields[7] = "-"
        else:
	    fields[7] = "{0:10.2f}".format((float)(fields[6])*100/(int)(fields[3]))
        if fields[9] == "0":
            fields[10] = "-"
        else:
	    fields[10] = "{0:10.2f}".format((float)(fields[8])/(int)(fields[9]))
	content = content + template.format(fields)
    dateFile.close()
    return content 

def sendMail(targetDate, html, conf):
    mailTo = conf.get('mail', 'to')
    mailSubject = conf.get('mail', 'title') +'['+targetDate.strftime("%Y-%m-%d")+']'
    mailFrom = conf.get('mail', 'from')
    mailSmtp = conf.get('mail', 'smtp')
    mailPort = conf.getint('mail', 'port')
    mailPswd = conf.get('mail', 'password')
    
    msg = MIMEMultipart()
    content = MIMEText(html,'html','utf-8')
    msg.attach(content)
    msg['To'] = mailTo
    msg['From'] = mailFrom
    msg['Subject'] = mailSubject
    try:
        s = smtplib.SMTP(mailSmtp, mailPort)
        s.login(mailFrom, mailPswd)
        s.set_debuglevel(0)
        s.sendmail(mailFrom, mailTo.split(';'), msg.as_string())
	time.sleep(5)
        s.quit()
    except smtplib.SMTPAuthenticationError as e:
        commonutil.error("send failed : error=[{0};{1}]".format(e.args[0], e.args[1]))

if __name__ == "__main__":
    d = os.path.dirname(__file__)
    if d != "" :
        os.chdir(d)
    #解析参数
    options = getOptions()
    targetDate = getTargetDate(options.targetDate)
    #准备工作
    outputPath = os.path.abspath("./output")+"/"+targetDate.strftime("%Y-%m-%d")
    commonutil.runCmd("mkdir -p", outputPath)
    mailConf = reportutil.getConf('mail.conf')
    dbConf = reportutil.getConf('db.conf')
    conns = reportutil.getConns(dbConf)
    targetDateStart = targetDate.strftime("%Y-%m-%d 00:00:00")
    targetDateEnd = (targetDate+timedelta(days=1)).strftime("%Y-%m-%d 00:00:00")
    targetDateEarly = (targetDate+timedelta(days=-7)).strftime("%Y-%m-%d 00:00:00")
    outputFile = outputPath+"/data"
    reportutil.truncateFile(outputFile)
    #拉取数据
    vars = {'VAR_START':targetDateStart, 'VAR_END':targetDateEnd, 'VAR_EARLY':targetDateEarly}
    isSuccess = dumpmysql.dump(conns['mall'], 'report.sql', outputFile, vars, True)
    if not isSuccess:
        commonutil.fatal("[{0}] failed".format(targetDateStart))
        sys.exit(1)
    commonutil.info("[{0}] done".format(targetDateStart))
    #生成报表
    html = reportutil.readFile('template.head')
    html = html + makeTrs('template.mid', outputFile)
    html = html + reportutil.readFile('template.tail')
    #发送邮件
    sendMail(targetDate, html, mailConf)

