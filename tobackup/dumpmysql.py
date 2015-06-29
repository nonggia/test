# -*- coding: utf8 -*-
from optparse import OptionParser
import sys
import os
import commonutil

#sys.argv =[sys.argv[0],'-s','./sql/dealgroup_tags.sql', '-o','./input/dealgroup_tags.2013-04-18', '-m', '10.1.1.217', '-d', 'TuanGou2010', '-u', 'tuan_analysis', '-w', 'dp!@7x7TWRilk', '-p', '3307']

fileDir = os.path.dirname(__file__)
if fileDir != "":
    os.chdir(fileDir)

import MySQLdb

def getOptions():
    parser = OptionParser()
    parser.add_option("-s", "--sql", dest="sql", help="sql file", metavar="FILE")
    parser.add_option("-o", "--output", dest="output", help="output file", metavar="FILE")
    parser.add_option("-m", "--mysql", dest="host", help="mysql host")
    parser.add_option("-u", "--user", dest="user", help="mysql user name")
    parser.add_option("-w", "--password", dest="password", help="mysql password name")
    parser.add_option("-p", "--port", dest="port", help="mysql port, default to 3306")
    parser.add_option("-d", "--database", dest="database", help="mysql db name")
    parser.add_option("-v", "--vars", dest="vars", help="vars as dict format")

    (options, args) = parser.parse_args()
    #print options
    if options.host is None or options.sql is None or options.output is None or options.database is None or options.user is None or options.password is None:
        print "ERROR : incomplete arguments"
        sys.exit(1)
    else:
        if options.port is None:
            print "WARNING : use default port 3306"
            options.port = 3306
        if options.vars is None:
            print "WARNING : use empty vars"
            options.vars = "{}"
    options.vars = eval(options.vars)

    return options

def dump(conn, sqlfileName, outfileName, vars={}, append=False):

    sqlfile = open(sqlfileName, "r")
    if append:
        outfile = open(outfileName, "a")
    else:
        outfile = open(outfileName, "w")

    sql = ""
    for line in sqlfile:
        sql = sql+line
    for varName in vars:
        sql = sql.replace(str(varName), str(vars[varName]))
    print sql 
    commonutil.debug("executing sql : sql=[{0}]".format(sql))
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
    except MySQLdb.Error as e:
        commonutil.error("execute sql failed : sql=[{0}] error=[{1};{2}]".format(sql, e.args[0], e.args[1]))
        return False

    for row in data:
        fields=[]
        for field in row:
            if field is None:
                strfield = "NULL"
            elif isinstance(field, unicode):
                strfield = field.encode("utf8")
            else:
                strfield = str(field)
            strfield = strfield.replace('\n', '')
            strfield = strfield.replace('\r', '')
            fields.append(strfield)
        outfile.write("\x01".join(fields)+"\n")

    cursor.close()
    outfile.close()
    sqlfile.close()
    return True

if __name__ == '__main__':
    options = getOptions();
    conn = commonutil.getConn(options.host, int(options.port), options.user, options.password, options.database)
    dump(conn, options.sql, options.output, options.vars)
    print "INFO : dump done"
