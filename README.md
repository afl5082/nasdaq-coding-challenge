# NASDAQ Coding Challenge 

I discovered this challenge through a computer science forum and thought it would be good practice combining my SQL and Python knowledge. The basis of the challenges worked with NASDAQ intraday stock data for four paticular stocks. The trade table holds all trades for four stocks on August 03, 2015. 

## Part 1

* For each stock, get the prices from the opening and closing cross trades on NASDAQ. 
* For each stock get the min, max, average and VWAP for consolidated last-sale eliglbe trades. 
* For each stock, get the total share volume and number of trades for volume-elgible trades
* Combine all of the results above in a single table, with one row per stock. 
*	Calculate the percent price range for each stock [use (max-min)/close].
*	Sort them from most to least volatile as measured by PctRange.
*	Write this table to a .csv 


## Part 2

* Summarize trading within each 5 minute period.
* Provide max, min, average and last price for each 5-minute time period for each stock (only include market hours 9:30-16:00) 


First step in Part 2 was to define the time chunks of a five minute period and match that with the timestamp variable in the database.

```
timebuckets = ("select a.RefDate, a.Symbol, cast(a.timestamp /300e3 as int) atimeBucket,\
time((cast(a.timestamp /300e3 as int) * 300000) /1000, 'unixepoch') as startTime.... 
```

## Part 3

* Match each last-sale eligible trade with the national best bid and offer that was in effect for the stock at the time when the trade occurred 
* The output files should only include the first 100 trades and trades 100,000 through 100,050


Snippet of code to find the closest value between bid and offers for the first 100 trades 


```
for i in trds_times[:100]:
	closest_value = min(qts_times, key=lambda x:(abs(x-i),x))
	position = qts_times.index(closest_value)
	if closest_value > i and b != 0:
		closest_value = qts_times[position-1]
		
	#IF CLOSEST VALUE IS GREATER THAN i (TRADE TS) THEN GO BACK 1
	
	qts_timesmatched.append(closest_value)
```

## Built With

* [sqlite3](https://docs.python.org/3/library/sqlite3.html#module-sqlite3) - Used to manage and query given database file
 
## Authors

* **Adam LaCaria** - *Initial work* - [Adam L](https://github.com/afl5082)


