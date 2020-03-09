"""ATTEMPT AT WEIGHTED AVERAGE EFFECTIVE SPREAD, SQLite/Python INSISTED ON CONVERTING
VALUES, QUICKER IN EXCEL BASED ON MY LIMITED KNOWLEDGE OF THIS FORMULA/ALGORITHIM"""

c.execute("CREATE TEMPORARY TABLE total_quan as select symbol, sum(quantity)as total_quant from trades_quotes group by symbol")

c.execute("select  a.symbol, sum( abs(price - ((askprice + bidprice )/ 2)) * \
(quantity / total_quant)  ) as effective_spread \
from trades_quotes a \
join qts b on qts_timestamp = b.timestamp \
join total_quan c on c.symbol = a.symbol group by a.symbol\
")
