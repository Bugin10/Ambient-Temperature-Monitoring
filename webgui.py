#!/usr/bin/env python

import sqlite3
import sys
import cgi
import cgitb

# global variables
speriod=(15*60)-1
dbname='templog.db'



# print the HTTP header
def printHTTPheader():
    print "Content-type: text/html\n\n"



# print the HTML head section
# arguments are the page title and the table for the chart
def printHTMLHead(title, table):
    print "<head>"
    print "    <title>"
    print title
    print "    </title>"
    
    print_graph_script(table)

    print "</head>"


# get data from the database
# if an interval is passed, 
# return a list of records from the database
def get_data(interval):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    if interval == None:
        curs.execute("SELECT * FROM temps")
    else:
        curs.execute("SELECT * FROM temps WHERE timestamp>datetime('now','-%s hours', 'localtime')" % interval)
#        curs.execute("SELECT * FROM temps WHERE timestamp>datetime('2013-09-19 21:30:02','-%s hours') AND timestamp<=datetime('2013-09-19 21:31:02')" % interval)

    rows=curs.fetchall()

    conn.close()

    return rows

# convert rows from database into a javascript table
def create_table(rows):
    chart_table=""

    for row in rows[:-1]:
        rowstr="['{0}', {1}, {2}],\n".format(str(row[0]),str(row[1]),str(row[2]))
        chart_table+=rowstr

    row=rows[-1]
    rowstr="['{0}', {1}, {2}]\n".format(str(row[0]),str(row[1]),str(row[2]))
    chart_table+=rowstr

    return chart_table


# print the javascript to generate the chart
# pass the table generated from the database info
def print_graph_script(table):

    # google chart snippet
    chart_code="""
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Time', 'Inside', 'Outside'],
%s
        ]);

        var options = {
          title: 'Temperature',
          explorer: {}
        };

        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>"""

    print chart_code % (table)




# print the div that contains the graph
def show_graph():
    print "<h2>Temperature Chart</h2>"
    print '<div id="chart_div" style="width: 90%; height: 50%; display:block; margin:auto"></div>'



# connect to the db and show some stats
# argument option is the number of hours
def show_stats(option):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    if option is None:
        option = str(24)

    curs.execute("SELECT timestamp,max(inside) FROM temps WHERE timestamp>datetime('now','-%s hour', 'localtime') AND timestamp<=datetime('now', 'localtime')" % option)
    rowmaxinside=curs.fetchone()
    rowstrmaxinside="{0}&nbsp&nbsp&nbsp{1}C".format(str(rowmaxinside[0]),str(rowmaxinside[1]))

    curs.execute("SELECT timestamp,min(inside) FROM temps WHERE timestamp>datetime('now','-%s hour', 'localtime') AND timestamp<=datetime('now', 'localtime')" % option)
    rowmininside=curs.fetchone()
    rowstrmininside="{0}&nbsp&nbsp&nbsp{1}C".format(str(rowmininside[0]),str(rowmininside[1]))

    curs.execute("SELECT avg(inside) FROM temps WHERE timestamp>datetime('now','-%s hour', 'localtime') AND timestamp<=datetime('now', 'localtime')" % option)
    rowavginside=curs.fetchone()


    curs.execute("SELECT timestamp,max(outside) FROM temps WHERE timestamp>datetime('now','-%s hour', 'localtime') AND timestamp<=datetime('now', 'localtime')" % option)
    rowmaxoutside=curs.fetchone()
    rowstrmaxoutside="{0}&nbsp&nbsp&nbsp{1}C".format(str(rowmaxoutside[0]),str(rowmaxoutside[1]))


    curs.execute("SELECT timestamp,min(outside) FROM temps WHERE timestamp>datetime('now','-%s hour', 'localtime') AND timestamp<=datetime('now', 'localtime')" % option)
    rowminoutside=curs.fetchone()
    rowstrminoutside="{0}&nbsp&nbsp&nbsp{1}C".format(str(rowminoutside[0]),str(rowminoutside[1]))

    curs.execute("SELECT avg(outside) FROM temps WHERE timestamp>datetime('now','-%s hour', 'localtime') AND timestamp<=datetime('now', 'localtime')" % option)
    rowavgoutside=curs.fetchone()





    print "<hr>"

    print "<table>"
    print "<td><h2>Minumum Temperature&nbsp</h2></td>"
    print "<tr><td><strong>Inside</strong></td></tr><tr><td>{0}</td></tr><td><strong>Outside</strong></td><tr><td>{1}</td></tr>".format(rowstrmininside,rowstrminoutside)
    print "<tr><td>&nbsp</td></tr>"
    print "<td><h2>Maximum Temperature</h2></td>"
    print "<tr><td><strong>Inside</strong></td></tr><tr><td>{0}</td></tr><td><strong>Outside</strong></td><tr><td>{1}</td></tr>".format(rowstrmaxinside,rowstrmaxoutside)
    print "<tr><td>&nbsp</td></tr>"
    print "<td><h2>Average Temperature</h2></td>"
    print "<tr><td><strong>Inside</strong></td></tr><tr><td>{0}</td></tr><td><strong>Outside</strong></td><tr><td>{1}</td></tr>".format(str("%.2f" % rowavginside),str("%.2f" % rowavgoutside))



    print "</table>"
    
    
    print "<hr>"

    print "<h2>In the last hour:</h2>"
    print "<table>"
    print "<tr><td><strong>Date/Time</strong></td><td><strong>Temperature</strong></td></tr>"

    rows=curs.execute("SELECT * FROM temps WHERE timestamp>datetime('now','-1 hour', 'localtime') AND timestamp<=datetime('now', 'localtime')")
#    rows=curs.execute("SELECT * FROM temps WHERE timestamp>datetime('2013-09-19 21:30:02','-1 hour') AND timestamp<=datetime('2013-09-19 21:31:02')")
    for row in rows:
        rowstr="<tr><td>{0}&emsp;&emsp;</td><td>{1}C&emsp;&emsp;</td><td>{2}C</td></tr>".format(str(row[0]),str(row[1]),str(row[2]))
        print rowstr
    print "</table>"

    print "<hr>"

    conn.close()




def print_time_selector(option):

    print """<form action="/cgi-bin/webgui.py" method="POST">
        Show the temperature logs for  
        <select name="timeinterval">"""


    if option is not None:

        if option == "6":
            print "<option value=\"6\" selected=\"selected\">the last 6 hours</option>"
        else:
            print "<option value=\"6\">the last 6 hours</option>"

        if option == "12":
            print "<option value=\"12\" selected=\"selected\">the last 12 hours</option>"
        else:
            print "<option value=\"12\">the last 12 hours</option>"

        if option == "24":
            print "<option value=\"24\" selected=\"selected\">the last 24 hours</option>"
        else:
            print "<option value=\"24\">the last 24 hours</option>"

        if option == "168":
            print "<option value=\"168\" selected=\"selected\">the last 7 days</option>"
        else:
            print "<option value=\"168\">the last 7 days</option>"

        if option == "72":
            print "<option value=\"72\" selected=\"selected\">the last month</option>"
        else:
            print "<option value=\"72\">the last month</option>"
    else:
        print """<option value="6">the last 6 hours</option>
            <option value="12">the last 12 hours</option>
            <option value="24">the last 24 hours</option>
            <option value="168">the last 7 days</option>
            <option value="72" selected="selected">the last month</option>"""

    print """        </select>
        <input type="submit" value="Display">
    </form>"""


# check that the option is valid
# and not an SQL injection
def validate_input(option_str):
    # check that the option string represents a number
    print "{0}".format(str(option_str))
    if option_str.isalnum():
        # check that the option is within a specific range
        if int(option_str) > 0 and int(option_str) <= 24:
            return option_str
        else:
            return None
    else: 
        return None


#return the option passed to the script
def get_option():
    form=cgi.FieldStorage()
    if "timeinterval" in form:
        option = form["timeinterval"].value
        return validate_input (option)
    else:
        return None




# main function
# This is where the program starts 
def main():

    cgitb.enable()

    # get options that may have been passed to this script
    option=get_option()

    if option is None:
        option = str(168)

    # get data from the database
    records=get_data(option)

    # print the HTTP header
    printHTTPheader()

    if len(records) != 0:
        # convert the data into a table
        table=create_table(records)
    else:
        print "No data found"
        return

    # start printing the page
    print "<html>"
    # print the head section including the table
    # used by the javascript for the chart
    printHTMLHead("Raspberry Pi Temperature Logger", table)

    # print the page body
    print "<body>"
    print "<h1>Raspberry Pi Temperature Logger</h1>"
    print "<hr>"
    print_time_selector(option)
    show_graph()

    show_stats(option)
    print "</body>"
    print "</html>"


    sys.stdout.flush()

if __name__=="__main__":
    main()





