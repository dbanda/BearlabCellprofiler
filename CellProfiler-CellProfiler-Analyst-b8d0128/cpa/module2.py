#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      Dalitso
#
# Created:     16/09/2012
# Copyright:   (c) Dalitso 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import csv

def creatTableFromCsv(filename):
    ifile  = open(filename, "rb")
    reader = csv.reader(ifile)
    header =  reader.next()
    headerVals =  reader.next()
    zipheader = zip(header,headerVals)

    columns = []
    def isnum(string):
        try:
            int(string)
            return True
        except:
            return False

    for i in zipheader:

        if isnum(i[1]):
            columns.append([i[0],'int'])
        else:
            columns.append([i[0],'varchar(255)'])

    columnheaders = '\n'.join([i[0] + ' ' + i[1] for i in columns])
    #print columnheaders

    query = 'CREATE TABLE ' + '`'+ 'pm.csv' + '` \n' + '( \n' + columnheaders +' \n)'
    print query


#filerow = set([i.lower().strip() for i in open('pm.csv').readlines(0)])
#print filerow