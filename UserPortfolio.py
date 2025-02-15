class UserPortfolio:
  def __init__(self, user_id, portfolio=None):
    self.user_id = user_id
    self.portfolio = portfolio if portfolio is not None else {}

  def update_portfolio(self, cusip, par, user_id):
    if cusip not in self.portfolio:
      self.portfolio[cusip] = 0
    self.portfolio[cusip] += par
    #for i in self.portfolio:
    #  if i != 'cash':
    #    db.update_portfolio(user_id=user_id, cusip=cusip, par=self.portfolio[i])
    db.update_portfolio(user_id, cusip, par)

  def has_sufficient_par(self, cusip, par):
    return self.portfolio[cusip] >= par

  def updated_cash(self, price, par, user_id):
    self.portfolio['cash'] += par * (price/100)
    #db.update_cash(user_id=user_id, cash=self.portfolio['cash'])

  def has_sufficient_cash(self, price, par, cash):
    return cash >= par * (price/100)


#Git push test