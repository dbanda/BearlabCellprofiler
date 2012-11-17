#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Dalitso
#
# Created:     16/09/2012
# Copyright:   (c) Dalitso 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from xlrd import open_workbook ,cellname
import MySQLdb

def xlstomysql(TableFromFile, filename, db )
    file_to_import = 'review_data_for_import.xls'
    column_count=6
    book = open_workbook(filename)
    sheet = book.sheet_by_index(0)
    print "Workbook sheet name:%s" % sheet.name
    print "Number of rows in sheet: %s" % sheet.nrows

# get a connection handle to MySQL
conn = MySQLdb.connect (host=db_host, user=db_user, passwd=db_passwd, db=db_database)

# get the cursor
cursor = conn.cursor()

# since we are using placeholders, we really only need to assign the query string sans values once, outside the loop
query = """INSERT INTO tblRawReviews (issue, company, product, reviewers, contact, review_text) VALUES (%s, %s, %s, %s, %s, %s)"""

# iterate through ieach row
for row_index in range(sheet.nrows):

        # we could assign the values directly in the values format string but this is easier to read
        row_num     = row_index
        issue_num   = sheet.cell(row_index,0).value
        company     = sheet.cell(row_index,1).value
        product     = sheet.cell(row_index,2).value
        reviewers   = sheet.cell(row_index,3).value
        contact     = sheet.cell(row_index,4).value
        review_text = sheet.cell(row_index,5).value

        # the row contents are different every time so we put this in the loop
        values = (issue_num, company, product, reviewers, contact, review_text)

        res = cursor.execute(query, values)

        # uncomment the next line to troubleshoot and see what's going on
        # print"row:%s data %s - %s - %s - %s - %s - %s" % (row_num, issue_num, company, product, reviewers, contact, review_text)

# close cursor
cursor.close()

# We are using an InnoDB tables so we need to commit the transaction
conn.commit()

#close connection
conn.close()
# Assign path to Excel file
file_to_import = 'review_data_for_import.xls'

# Assign column count
# This can be detected but to get a subset
# of the existing column cells I assign it manually
column_count=6

# open the entire workbook
# you can work with multiple page workbooks
book = open_workbook(file_to_import)

# we are only using the first sheet
sheet = book.sheet_by_index(0)

# Why not?
print "Workbook sheet name:%s" % sheet.name
print "Number of rows in sheet: %s" % sheet.nrows

# get a connection handle to MySQL
conn = MySQLdb.connect (host=db_host, user=db_user, passwd=db_passwd, db=db_database)

# get the cursor
cursor = conn.cursor()

# since we are using placeholders, we really only need to assign the query string sans values once, outside the loop
query = """INSERT INTO tblRawReviews (issue, company, product, reviewers, contact, review_text) VALUES (%s, %s, %s, %s, %s, %s)"""

# iterate through ieach row
for row_index in range(sheet.nrows):

        # we could assign the values directly in the values format string but this is easier to read
        row_num     = row_index
        issue_num   = sheet.cell(row_index,0).value
        company     = sheet.cell(row_index,1).value
        product     = sheet.cell(row_index,2).value
        reviewers   = sheet.cell(row_index,3).value
        contact     = sheet.cell(row_index,4).value
        review_text = sheet.cell(row_index,5).value

        # the row contents are different every time so we put this in the loop
        values = (issue_num, company, product, reviewers, contact, review_text)

        res = cursor.execute(query, values)

        # uncomment the next line to troubleshoot and see what's going on
        # print"row:%s data %s - %s - %s - %s - %s - %s" % (row_num, issue_num, company, product, reviewers, contact, review_text)

# close cursor
cursor.close()

# We are using an InnoDB tables so we need to commit the transaction
conn.commit()

#close connection
conn.close()
def main():
    pass

if __name__ == '__main__':
    main()
