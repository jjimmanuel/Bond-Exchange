class DataBase:
  def __init__(self, database_file="MUNI_EXCHANGE.db"):
    self.connection = sqlite3.connect(database_file)
    self.cursor = self.connection.cursor()
    self.create_tables()

  def create_tables(self):
    self.cursor.execute(
        '''CREATE TABLE IF NOT EXISTS users (
          user_id TEXT,
          created_at TEXT
        )'''
    )

    self.cursor.execute(
        '''CREATE TABLE IF NOT EXISTS portfolios (
          user_id TEXT,
          cusip TEXT,
          par INTEGER
        )'''
    )

    self.cursor.execute(
        '''CREATE TABLE IF NOT EXISTS cash (
          user_id TEXT,
          cash REAL
        )'''
    )

    self.cursor.execute(
        '''CREATE TABLE IF NOT EXISTS orders (
          user_id TEXT,
          order_id INTEGER,
          order_type TEXT,
          cusip TEXT,
          price REAL,
          par INTEGER,
          side TEXT
        )'''
    )

    self.cursor.execute(
        '''CREATE TABLE IF NOT EXISTS trades (
          buyer_id TEXT,
          seller_id TEXT,
          price REAL,
          par INTEGER,
          cusip TEXT,
          time_of_trade TEXT
        )'''
    )

    self.cursor.execute(
        '''CREATE TABLE IF NOT EXISTS notifications (
          user_id TEXT,
          cusip TEXT,
          side TEXT
    )'''
    )

  def update_users(self, user_id):
    time = datetime.now()
    self.cursor.execute("INSERT INTO users (user_id, created_at) VALUES (?, ?)", (user_id, time))
    self.connection.commit()

  def update_portfolio(self, user_id, cusip, par):
    self.cursor.execute("SELECT user_id, cusip FROM portfolios WHERE user_id = ? and cusip = ?", (user_id, cusip))
    result = self.cursor.fetchall()
    print(result)
    if result:
      self.cursor.execute("UPDATE portfolios SET par = par + ? WHERE user_id = ? AND cusip = ?", (par, user_id, cusip))
    else:
      self.cursor.execute("INSERT INTO portfolios (user_id, cusip, par) VALUES (?, ?, ?)", (user_id, cusip, par))

    self.connection.commit()

  def update_cash(self, user_id, cash):
    self.cursor.execute("SELECT user_id, cash FROM cash WHERE user_id = ?", (user_id,))
    result = self.cursor.fetchone()
    if result:
      self.cursor.execute("UPDATE cash SET cash = cash + ? WHERE user_id = ?", (cash, user_id))
    else:
      self.cursor.execute("INSERT INTO cash (user_id, cash) VALUES (?, ?)", (user_id, cash))

    self.connection.commit()

  def update_orders(self, user_id, order_id, order_type, cusip, price, par, side):
    self.cursor.execute("INSERT INTO orders (user_id, order_id, order_type, cusip, price, par, side) VALUES (?, ?, ?, ?, ?, ?, ?)", (user_id, order_id, order_type, cusip, price, par, side))
    self.connection.commit()

  def cancel_orders(self, user_id, order_id):
    self.cursor.execute("DELETE FROM orders WHERE user_id = ? AND order_id = ?", (user_id, order_id))
    self.connection.commit()

  def update_trades(self, buyer_id, seller_id, cusip, price, par):
    time = datetime.now()
    self.cursor.execute("INSERT INTO trades (buyer_id, seller_id, cusip, price, par, time_of_trade) VALUES (?, ?, ?, ?, ?, ?)", (buyer_id, seller_id, cusip, price, par, time))
    self.connection.commit()

  def update_notifications(self, user_id, cusip, side):
    self.cursor.execute("INSERT INTO notifications (user_id, cusip) VALUES (?, ?)", (user_id, cusip))
    self.connection.commit()

  def check_ns(self, user_id, cusip, side):
    self.cursor.execute("SELECT user_id, cusip FROM notifications WHERE user_id = ? AND cusip = ? AND side = ?", (user_id, cusip, side))
    results = self.cursor.fetchall()
    return results

  def in_orderbook(self, user_id, cusip, side):
    self.cursor.execute("SELECT cusip from orders where user_id = ? AND cusip = ? AND side = ?", (user_id, cusip, side))
    results = self.cursor.fetchall()
    return results
