This is just a 'code dump' for how a bond exchange might work. I wrote this code just so I can work through how a MarketAxess/TradeWeb/Trumid type of product might match and execute different types of orders.
The code contains classes for a Database (SQLite), Orders, Portfolios, a Matching Engine, Dutch Auctions, and Notifications. Within the Matching Engine class and the Dutch Auction class, I tried my hand at Python's asyncio package to hold hold mutiple auctions simulatenously rather than sequentially (same for order matching), but clearly I am not very good at it. I will be making periodic updates over time. 


