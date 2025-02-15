class DutchAuction:
  def __init__(self, auction_id, user_id, cusip, par, start_price, reserve_price, price_step, current_price, timestep):
    self.user_id = user_id
    self.cusip = cusip
    self.par = par
    self.start_price = start_price
    self.reserve_price = reserve_price
    self.price_step = price_step
    self.auction_id = auction_id
    self.current_price = start_price
    self.timestep = timestep

class Bid:
  def __init__(self, user_id, price, auction_id):
    self.user_id = user_id
    self.price = price
    self.auction_id = auction_id