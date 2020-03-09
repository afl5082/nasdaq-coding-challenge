
import sqlite3
import csv
import pandas.io.sql as sql
conn = sqlite3.connect('nqdb3.db')

c = conn.cursor()

"""---OVERALL METHOD WAS TO CREATE MULTIPLE TEMP TABLES AND JOIN FOR ANALYSIS
 		THIS WAS QUICKER THAN MULTIPLE SUBQUERIES """


#--PREVIEW TABEL DATA
#res = c.execute("SELECT name from sqlite_master where type = 'table';")

#for name in res:
	#print (name[0])
	
#print(c.fetchall())
#trds, qts

#c.execute("PRAGMA table_info(trds)")

#--TEMP TABLE FOR BASE STATS 
c.execute( "CREATE TEMPORARY TABLE trds_stats as  \
select max(price) as MaxPrice , refdate ,min(price) MinPrice, avg(price) AvgPrice, ((sum(price * quantity))  / (sum(quantity) )) as VWAP ,  Symbol from  trds \
where salecondition not like '%G%' \
and salecondition not LIKE '%I%' \
and salecondition not LIKE '%H%' \
and salecondition not LIKE '%C%' \
and salecondition not LIKE '%M%' \
and salecondition not LIKE '%N%' \
and salecondition not LIKE '%P%' \
and salecondition not LIKE '%Q%' \
and salecondition not LIKE '%R%' \
and salecondition not LIKE '%T%' \
and salecondition not LIKE '%U%' \
and salecondition not LIKE '%V%' \
and salecondition not LIKE '%W%' \
and salecondition not LIKE '%Z%' \
and salecondition not LIKE '%4%' \
and salecondition not LIKE '%7%' \
group by symbol"
)

"""--TEMP TABLE FOR OPEN STAT"""
c.execute("CREATE TEMPORARY TABLE trds_open as select symbol, price as OpeningPrice \
from trds where salecondition = 'Q' and pid = 'Q'  group by symbol")

"""--TEMP TABLE FOR CLOSE STAT"""
c.execute("CREATE TEMPORARY TABLE trds_close as select symbol, price as ClosingPrice \
from trds where salecondition LIKE '%M%' and pid = 'Q'  group by symbol")

"""--TEMP TABLE FOR VOLUME STATS"""
c.execute("CREATE TEMPORARY TABLE trds_volume as select symbol, count(symbol) as Trades, sum(quantity)  as Shares \
from trds \
where salecondition not like '%M%' \
and salecondition not like '%Q%' \
and salecondition not like '%9%' \
group by symbol")

"""--TEMP TABLE FOR FINAL ANALYSIS, JOINING PREVIOUS TEMP TABLES"""
c.execute("CREATE TEMPORARY TABLE trds_daysum as Select a.refdate, a.symbol, b.openingprice, c.closingprice, \
a.minprice, a.maxprice, a.avgprice, a.vwap, \
e.trades, e.shares, ((a.maxprice - a.minprice) / c.closingprice) as PctRange \
from trds_stats as a join trds_open as b on a.symbol = b.symbol \
join trds_close as c on c.symbol = b.symbol \
join trds_volume as e on e.symbol = b.symbol group by a.symbol order by pctrange DESC")

table = sql.read_sql('select * from trds_daysum', conn)
table.to_csv('DaySummary_v02.csv')

# 'G'|'I'|'H'|'M'|'C'|'N'|'R'|'P'|'Q'|'T'|'U'|'V'|'W'|'Z'|'4' group by symbol" )






