# NASDAQ Code Challenge 

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


And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

## Built With

* [sqlite3](https://docs.python.org/3/library/sqlite3.html#module-sqlite3) - Used to manage and query given database file
 
## Authors

* **Adam LaCaria** - *Initial work* - [Adam L](https://github.com/afl5082)


