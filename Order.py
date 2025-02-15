class Order:
  def __init__(self, order_id, order_type, par, cusip, price, side, user_id):
    self.order_id = order_id
    self.order_type = order_type
    self.par = par
    self.cusip = cusip
    self.price = price
    self.side = side
    self.user_id = user_id