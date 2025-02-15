class MatchingEngine:
  def __init__(self, db):
    self.db = db
    self.buy_orders = []
    self.sell_orders = []
    self.order_counter_id = 1
    self.trade_history = []
    self.users = {}
    self.order_map = {}

  def add_user(self, user_id, portfolio):
    if user_id not in self.users:
      self.users[user_id] = UserPortfolio(user_id, portfolio)
      db.update_users(user_id=user_id)
      for i in self.users[user_id].portfolio:
        if i != 'cash':
          db.update_portfolio(user_id=user_id, cusip=i, par=self.users[user_id].portfolio[i])
        else:
          break
      db.update_cash(user_id=user_id, cash=self.users[user_id].portfolio['cash'])
    else:
      print("This user already exists")


  def add_order(self, order_type, par, cusip, price, side, user_id):
    order = Order(order_id=self.order_counter_id, par=par, cusip=cusip, price=price, side=side, user_id=user_id, order_type=order_type)
    db.update_orders(user_id=user_id, order_id=self.order_counter_id, order_type=order_type, cusip=cusip, price=price, par=par, side=side)
    self.order_counter_id += 1
    self.order_map[order.order_id] = order
    print(self.order_map)
    print(order)

    cash = self.users[user_id].portfolio['cash']
    #print(cash)

    if order.side == "sell" and self.users[user_id].has_sufficient_par(cusip, par) == False:
      print("Insufficient Par to Place a Sell Order")
    else:
      print("Sufficient ")

    if order.side == 'buy' and self.users[user_id].has_sufficient_cash(par, price, cash) == False:
      print("Insuffient Cash to Place a Buy Order")
    else:
      print("Sufficient Cash Available")


    if order.order_type == 'limit':
      self._process_limit_order(order, cusip)

    elif order.order_type == 'market':
      self._process_market_order(order, cusip)

  def cancel_sell_order(self, user_id, order_id):
    db.cancel_orders(user_id=user_id, order_id=order_id)
    for item in self.sell_orders:
      if item[1] == order_id:
        self.sell_orders.remove(item)
        break

    print(self.sell_orders)


  def _process_limit_order(self, order, cusip):

    if order.par > 0:
      if order.side == "buy":
        heapq.heappush(self.buy_orders, (-order.price, order.order_id, order))

      elif order.side == "sell":
        heapq.heappush(self.sell_orders, (order.price, order.order_id, order))


    self._match_limit_order(order, cusip)
    print(self.sell_orders)

  def _match_limit_order(self, incoming_order, cusip):
    if incoming_order.side == "buy":
      while incoming_order.par > 0 and self.sell_orders:
        best_sell_price, _, best_sell_order = self.sell_orders[0]

        if best_sell_order.par == 0:
          heapq.heappop(self.sell_orders)
          continue

        if incoming_order.price < best_sell_price:
          break

        if (incoming_order.par == best_sell_order.par and
            incoming_order.price == best_sell_order.price):

          self._execute_market_order(incoming_order, best_sell_order, cusip)

        else:
          break


    elif incoming_order.side == "sell":
      while incoming_order.par > 0 and self.buy_orders:
        best_buy_price, _, best_buy_order = self.buy_orders[0]
        best_buy_price = -best_buy_price

        if best_buy_order.par == 0:
          heapq.heappop(self.buy_orders)
          continue

        if incoming_order.price > best_buy_price:
          break

        if (incoming_order.par == best_buy_order.par and
            incoming_order.price == best_buy_order.price):

          self._execute_market_order(incoming_order, best_buy_order, cusip)

        else:
          break



  def _process_market_order(self, order, cusip):
    self._match_market_order(order, cusip)

    if order.par > 0:
      if order.side == "buy":
        heapq.heappush(self.buy_orders, (-order.price, order.order_id, order))
      elif order.side == "sell":
        heapq.heappush(self.sell_orders, (order.price, order.order_id, order))


  def _match_market_order(self, incoming_order, cusip):
    if incoming_order.side == "buy":
      while incoming_order.par > 0 and self.sell_orders:
        best_sell_price, _, best_sell_order = self.sell_orders[0]

        if best_sell_order.par == 0:
          heapq.heappop(self.sell_orders)  # Remove from heap
          continue

        if incoming_order.price < best_sell_price:
          break

        self._execute_market_order(incoming_order, best_sell_order, cusip)

    elif incoming_order.side == "sell":
      while incoming_order.par > 0 and self.buy_orders:
        best_buy_price, _, best_buy_order = self.buy_orders[0]
        best_buy_price = -best_buy_price  # Convert back to positive

        if best_buy_order.par == 0:
          heapq.heappop(self.buy_orders)  # Remove from heap
          continue

        if incoming_order.price > best_buy_price:
          break

        self._execute_market_order(incoming_order, best_buy_order, cusip)

  def _execute_market_order(self, incoming_order, counter_order, cusip):

    if incoming_order.par == 0 or counter_order.par == 0:
      return

    trade_par = min(incoming_order.par, counter_order.par)
    incoming_order.par -= trade_par
    counter_order.par -= trade_par


    trade_price = counter_order.price if incoming_order.side == "buy" else incoming_order.price

    # Log trade
    trade = {
            "buyer": incoming_order.user_id if incoming_order.side == "buy" else counter_order.user_id,
            "seller": counter_order.user_id if incoming_order.side == "buy" else incoming_order.user_id,
            "price": trade_price,
            "par": trade_par,
            "cusip": cusip
        }
    self.trade_history.append(trade)
    db.update_trades(buyer_id=self.users[trade["buyer"]].user_id, seller_id=self.users[trade['seller']].user_id, cusip=cusip, price=trade_price, par=trade_par)
    print(f"Trade Executed: {trade}")

    # Update portfolios
    buyer = self.users[trade["buyer"]]
    seller = self.users[trade["seller"]]
    buyer.update_portfolio(cusip, trade_par, buyer.user_id)
    seller.update_portfolio(cusip, -trade_par, seller.user_id)
    #db.update_portfolio(user_id=buyer.user_id, cusip=cusip, par=trade_par)
    #db.update_portfolio(user_id=seller.user_id, cusip=cusip, par=-trade_par)
    buyer.updated_cash(price=trade_price, par=-trade_par, user_id=buyer.user_id)
    seller.updated_cash(price=trade_price, par=trade_par, user_id=seller.user_id)
    db.update_cash(user_id=buyer.user_id, cash=-trade_par*(trade_price/100))
    db.update_cash(user_id=seller.user_id, cash=trade_par*(trade_price/100))

    if counter_order.par == 0:
      if counter_order.side == "sell":
        heapq.heappop(self.sell_orders)
      elif counter_order.side == "buy":
        heapq.heappop(self.buy_orders)

  def print_user_portfolio(self, user_id):
    if user_id in self.users:
      user = self.users[user_id]
      print(f"Portfolio for User {user_id}: {user.portfolio}")
    else:
      print(f"User {user_id} does not exist.")


  def print_order_book(self):
    print("\nOrder Book:")

    print("Buy Orders:")
    for price, _, order in sorted(self.buy_orders, reverse=True):
      if order.par != 0:
        print(f" {order}")


    print("Sell Orders:")
    for price, _, order in sorted(self.sell_orders):
      if order.par != 0:
        print(f"  {order.par}")

  def print_trade_history(self):
    print("\nTrade History:")
    for trade in self.trade_history:
      print(trade)
