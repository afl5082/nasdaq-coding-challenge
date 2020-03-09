
import sqlite3
import csv
import pandas.io.sql as sql
conn = sqlite3.connect('nqdb3.db')

c = conn.cursor()

"""-- OVERALL METHOD WAS TO SEPERATE LASTPRICE AND OTHER STATS DUE TO LASTPRICE
	BEING TRICKIER TO GET WITHIN A SUBET OF THE TIMEBUCKETS"""


"""TEMP TABLE FOR LASTPRICE, PRIMARY KEY IS TIMEBUKET
#SUBQUERY TO SELECT THE ROWID WHERE MAX ROWID IS IN GROUPING OF EACH TIMEBUCKET"""

c.execute("CREATE TEMPORARY TABLE trds_lastprice as Select price,symbol,cast(timestamp/300e3 as int) as btimeBucket from trds where rowid in  \
(select max(rowid) from trds where salecondition not like '%I%' \
and salecondition not like '%W%' \
and salecondition not like '%7%' \
and salecondition not like '%V%' \
and salecondition not like '%C%' \
and salecondition not like '%H%' \
and salecondition not like '%9%' \
and salecondition not like '%N%' \
and salecondition not like '%R%' \
and salecondition not like '%T%' \
and salecondition not like '%G%' \
and salecondition not like '%P%' \
and salecondition not like '%U%' \
and salecondition not like '%4%' \
and salecondition not like '%Q%' \
and salecondition not like '%M%' \
and salecondition not like '%Z%' \
group by symbol, cast(timestamp/300e3 as int)) \
 ") 



"""TABLE FOR CSV OUTPUT#CREATED STARTIME BASED ON TIMEBUKET AND 5 MIN INCREMENTS 
GRABBING LAST PRICE FROM PREVIOUS TEMP TABLE BY JOINING ON TIMEBUCKET"""

timebuckets = ("select a.RefDate, a.Symbol, cast(a.timestamp /300e3 as int) atimeBucket,\
time((cast(a.timestamp /300e3 as int) * 300000) /1000, 'unixepoch') as startTime,\
max(a.price) as MaxPrice ,min(a.price) MinPrice, avg(a.price) AvgPrice, b.price as LastPrice \
from trds a join trds_lastprice as b on a.symbol = b.symbol and cast(timestamp/300e3 as int)  = btimeBucket \
where timestamp  >= '34200000' and timestamp <= '57600000' \
AND salecondition not like '%I%' \
AND salecondition not like '%W%' \
and salecondition not like '%7%' \
and salecondition not like '%V%' \
and salecondition not like '%C%' \
and salecondition not like '%H%' \
and salecondition not like '%9%' \
and salecondition not like '%N%' \
and salecondition not like '%R%' \
and salecondition not like '%T%' \
and salecondition not like '%G%' \
and salecondition not like '%P%' \
and salecondition not like '%U%' \
and salecondition not like '%4%' \
and salecondition not like '%Q%' \
and salecondition not like '%M%' \
and salecondition not like '%Z%' \
group by a.Symbol, atimeBucket order by a.Symbol, atimeBucket ASC")
 
table = sql.read_sql(timebuckets, conn)
table.to_csv('FiveMins_v02.csv')

print(c.fetchall())





#timebuckets = ("select RefDate, Symbol, cast(timestamp /300e3 as int) timeBucket,\
#time((cast(timestamp /300e3 as int) * 300000) /1000, 'unixepoch') as startTime,\
#max(price) as MaxPrice ,min(price) MinPrice, avg(price) AvgPrice \
#from trds where timestamp  >= '34200000' and timestamp <= '57600000' \
#group by Symbol, timeBucket order by Symbol, timeBucket ASC")


