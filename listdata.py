#!/usr/bin/env python
print "Content-type: text/html\n\n"
print "<h1>Hello World</h1>"
import sqlite3

conn=sqlite3.connect('templog.db')
curs=conn.cursor()

print "<table>"
rows=curs.execute("SELECT * FROM temps WHERE timestamp>datetime('now','-100000000 hour', 'localtime') AND timestamp<=datetime('now', 'localtime') ORDER BY timestamp DESC")
#    rows=curs.execute("SELECT * FROM temps WHERE timestamp>datetime('2013-09-19 21:30:02','-1 hour') AND timestamp<=datetime('2013-09-19 $
for row in rows:
	rowstr="<tr><td>{0}&emsp;&emsp;</td><td>{1}C&emsp;&emsp;</td><td>{2}C&emsp;&emsp;</td><td>{3}%&emsp;&emsp;</td><td>{4}%&emsp;&emsp;</td></tr>".format(str(row[0]),str(row[1]),str(row[2]), str(row[3]), str(row[4]))
	print rowstr
print "</table>"

