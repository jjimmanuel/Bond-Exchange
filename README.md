Some code detailing how a bond matching engine might work. I wrote this code just so I can understand for myself how a MarketAxess/TradeWeb/Trumid type of product might match and execute different types of orders.
The code contains classes for a Database (SQLite), Orders, Portfolios, a Matching Engine, Dutch Auctions, and Notifications. While ordinary limit/market orders are matched sequentially, I allowed Dutch Auctions to be held asynchronously as auctions take much longer to execute by their nature. 


