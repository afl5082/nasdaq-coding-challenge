
import sqlite3
import csv
import pandas.io.sql as sql
import numpy
conn = sqlite3.connect('nqdb3.db')

"""--OVERALL METHOD WAS TO USE A PYTHON FUNCTION INSTEAD OF A SQL FUNCTION
TO EXTRACT NEAREST K (N) VALUES. ONCE THIS WAS DONE - I INSERTED THOSE VALUES
BACK INTO THE TRADES TABLE WITH EACH ROW HAVING A TIMESTAMP FROM THE QUOTES TABLE
THAT IS LESS THAN OR EQUAL, I THEN JOINED THAT MODIFIED TABLE ON QUOTES TO GET
QUOTE DATA, NAMELY BID/ASK PRICE """

"""WRITING TO LISTS FROM QUERIES DIRECTLY"""
conn.row_factory = lambda cursor, row: row[0]

c = conn.cursor()


"""GATHERING TIMESTAMPS FROM EACH TABLE AND PUTTING THEM IN A LIST"""
qts_times = c.execute('SELECT timestamp FROM qts where timestamp >= 34200000 and \
timestamp <= 57600000').fetchall()

trds_times = c.execute("SELECT timestamp FROM trds where timestamp >= 34200000 and \
timestamp <= 57600000 and symbol = 'MSFT' and \
salecondition not like '%G%' \
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
and salecondition not LIKE '%7%'").fetchall()

"""SLICING ONLY THE FIRST 100 VALUES AND LAST 50.
LOOPING THROUGH EACH USING A MIN LAMBDA FUNCTION TO EXTRACT NEAREST LESS THAN
VALUE. NOTE: I DID HAVE TO THROW IN AN IF BLOCK FOR AN ERROR IN ONE LAMBDA INSTANCE"""

qts_timesmatched =[]
trds_timesmatched =[]
#WILL APPEND MATCHED VALUES INTO THESE LISTS, TO LATER BE INSERTED INTO TRDS
b = 0
for i in trds_times[:100]:
	#closest_value = min(qts_times, key=lambda x: (abs(x-i),x))
	closest_value = min(qts_times, key=lambda x:abs(x-i))
	if closest_value > i:
		closest_value = qts_times[b-1]
	#IF CLOSEST VALUE IS GREATER THAN i (TRADE TS) THEN GO BACK 1
	
	qts_timesmatched.append(closest_value)
	trds_timesmatched.append(i)
	
for i in trds_times[100000:100051]:
	closest_value = min(qts_times, key=lambda x: (abs(x-i),x))
	
	qts_timesmatched.append(closest_value)
	trds_timesmatched.append(i)
	
print(trds_timesmatched[5])
#TEST ^

conn.close()
conn = sqlite3.connect('nqdb3.db')  
#close and reopen connecton to rid row settings OR WRITING TO LIST
c = conn.cursor()

"""TEMP TABLE FOR FIRST 100"""
c.execute("CREATE TEMPORARY TABLE tq1 as select * from trds \
where timestamp >= 34200000 and \
timestamp <= 57600000 and symbol = 'MSFT' and \
salecondition not like '%G%' \
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
and salecondition not LIKE '%7%' limit 100 ")

"""TEMP TABLE FOR LAST 50"""
c.execute("CREATE TEMPORARY TABLE tq2_first as select * from trds \
where timestamp >= 34200000 and \
timestamp <= 57600000 and symbol = 'MSFT' and \
salecondition not like '%G%' \
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
and salecondition not LIKE '%7%' ")

"""ROW IDS WERE BEING MESSED DUE TO OTHER PARAMETERS
A SECOND TEMP TABLE FOR LAST 50"""

c.execute("CREATE TEMPORARY TABLE tq2 as select * from tq2_first \
where rowid >= 100000 and rowid <= 100050")

"""UNIONING FIRST 100 AND LAST 50"""
c.execute("CREATE TEMPORARY TABLE trades_quotes as  select * from tq1 union all select * from tq2")

"""CREATING COLUMN FOR NEAREST QUOTE TIMESTAMP"""
c.execute("ALTER TABLE trades_quotes ADD COLUMN qts_timestamp  ")

"""INSERTING TIMESTAMP INTO EACH ROW, CORRESPONDING TO RESPECTIVE ROWID"""
rowid = 1;
for item in qts_timesmatched:
	c.execute("UPDATE trades_quotes set qts_timestamp = ? where rowid = ? ",(item,rowid))
	rowid = rowid +1


"""SELECTING ONLY WHAT IS NEEDED AND WRITING TO CSV"""
t_q = ("select a.refdate, a.symbol, a.timestamp,bidprice, askprice, \
price, quantity, pid  from trades_quotes a \
join qts b on qts_timestamp = b.timestamp")

table = sql.read_sql(t_q, conn)
table.to_csv('TradesAndQuotes_v02.csv')
#print(c.fetchall())




# trades_quotes = ("select * from trds a join qts b on \
# b.timestamp = (select c.timestamp from qts c \
# where c.timestamp <=  a.timestamp  \
# order by c.timestamp DESC limit 1) limit 10")


# table = sql.read_sql(trades_quotes, conn)
# table.to_csv('trades_quotes.csv')
# print(c.fetchall())


# "select * from trds a join qts b on a.timestamp = b.timestamp and a.symbol = b.symbol \
# where salecondition not like '%W%' \
# and salecondition not like '%I%' \
# and salecondition not like '%7%' \
# and salecondition not like '%V%' \
# and salecondition not like '%C%' \
# and salecondition not like '%H%' \
# and salecondition not like '%9%' \
# and salecondition not like '%N%' \
# and salecondition not like '%R%' \
# and salecondition not like '%T%' \
# and salecondition not like '%G%' \
# and salecondition not like '%P%' \
# and salecondition not like '%U%' \
# and salecondition not like '%4%' \
# and salecondition not like '%Q%' \
# and salecondition not like '%M%' \
# and salecondition not like '%Z%' \
# limit 100"


#https://stackoverflow.com/questions/11853167/parameter-unsupported-when-inserting-int-in-sqlite
