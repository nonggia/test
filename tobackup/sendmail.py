# -*- coding: utf8 -*-

import smtplib
from datetime import datetime, timedelta
import time
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart

def get_html_msg(send_date):
     head = """<head><meta charset="utf-8">
    <STYLE TYPE="text/css" MEDIA=screen>
    <!--
     table {font-size:20px;border-collapse: collapse;font-family: arial;}
    thead {border: 2px solid #B1CDE3;background: #00ffff;font-size:18px;padding: 10px 10px 10px       10px;color: #4f6b72;font-family: times;}
     th {vertical-align:top;font-size:12px;padding: 5px 5px 5px 5px;color: #4f6b72;font-family: arial;}
     body {font-family: arial;}
    -->
    </STYLE>
    </head>"""

     p = """<p>大家好：<br>截止到 xxxxx,各个设备性     能指标报表如下，请查阅。<br></p>"""

     body = """<body>""" + p + """
     <table border="0" cellpadding="0" cellspacing="0">
     <th>aaaaaaaaaa</th>
     <th>bbbbbbbbbb</th>
     </table>
     </body>"""
     html = """<html>""" + head + body + """</html>"""
     return html

def send_mail(html_msg):
     msg = MIMEMultipart()
     content = MIMEText(html_msg,'html')
     msg.attach(content)
     msg['To'] = ";".join(['liangjiangzhang@loukou.com'])
     msg['From'] = 'liangjiangzhang@loukou.com'
     msg['Subject'] = 'i am a subject'
     s = smtplib.SMTP('smtp.263.net', 25)
     s.login('liangjiangzhang@loukou.com', '')
     s.set_debuglevel(0)
     s.sendmail('liangjiangzhang@loukou.com', ['liangjiangzhang@loukou.com'], msg.as_string())
     s.quit()
     print "ok"

if __name__ == "__main__":
     now = datetime.now() 
     html = get_html_msg('immsg')
     send_mail(html)
