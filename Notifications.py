class Notification:
  def __init__(self, user_id, cusip, side):
    self.cusip = cusip
    self.user_id = user_id
    self.side = side

class MatchNotifications:
  def __init__(self, db):
    self.db = db
    self.notifications = []

  def create_notification(self, user_id, cusip, side):
    notification = Notification(user_id, cusip , side)
    db.update_notifications(user_id=user_id, cusip=cusip, side=side)
    self.notifications.append((notification.user_id, notification.cusip, notification.side))

  def check_notification(self, user_id, cusip):
    results = db.check_ns(user_id=user_id, cusip=cusip)
    if (user_id, cusip) in results:
      return "A notifitcation exists for this cusip"

  def cusip_in_orderbook(self, user_id, cusip, side):
    orderbook_results = db.in_orderbook(user_id=user_id, cusip=cusip, side=side)
    notification_results = db.check_ns(user_id=user_id, cusip=cusip, side=side)
    string = f"The CUSIP: {cusip} is available for {side}"
    if (user_id, cusip, side) in orderbook_results and notification_results:
      return string

  def trade_confirmation(self, buyer_id=None, seller_id=None, cusip, par, price):
    buyer_id = buyer_id if not None else None
    seller_id = seller_id if not None else None
