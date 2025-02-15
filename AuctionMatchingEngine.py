class MatchingAuction:
  def __init__(self, db):
    self.db = db
    self.active_auctions = {}
    self.bids = []
    #self.bids_user_id = []
    self.auction_counter_id = 1
    self.id_matches = []
    self.lock = asyncio.Lock()
    self.

  def create_auction(self, user_id, cusip, par, start_price, reserve_price, price_step, current_price, timestep):
    auction = DutchAuction(auction_id=self.auction_counter_id, user_id=user_id, cusip=cusip, par=par, start_price=start_price, reserve_price=reserve_price, price_step=price_step, current_price=start_price, timestep=timestep)
    self.active_auctions[auction.auction_id] = auction
    self.auction_counter_id += 1
    #self._update_auction()

  async def place_bid(self, user_id, auction_id, price):
    bid = Bid(user_id=user_id, auction_id=auction_id, price=price)
    #auction = self.active_auctions[auction_id]
    heapq.heappush(self.bids, (bid.price, bid.auction_id, bid.user_id))
    heapq.heapify(self.bids)
    #heapq.heappush(self.bids_user_id, (bid.user_id, bid.auction_id))

    await self._match_bid(auction_id=auction_id)



  async def _update_auction(self):
    while self.active_auctions:

    #for i in self.active_auctions.items():
      for auction_id, auction in list(self.active_auctions.items()):
        #auction = i[1]
        await asyncio.sleep(5)
        match_result = await self._match_bid(auction_id)
        best_buy_price, user, id = match_result
        if auction.current_price <= auction.reserve_price:
          del self.active_auctions[auction.auction_id]
          continue
        elif auction.current_price == best_buy_price and auction.auction_id == id:
          print(f"For auction {auction_id}, the bond with cusip {auction.cusip} sold at a price of {auction.current_price}")

          #Update Portfolios
          seller_id = auction.user_id
          buyer_id = user
          cusip = auction.cusip
          par = auction.par
          seller = engine.users[seller_id]
          buyer = engine.users[buyer_id]
          seller.update_portfolio(cusip=cusip, par=-par, user_id=seller.user_id)
          buyer.update_portfolio(cusip=cusip, par=par, user_id=buyer.user_id)
          db.update_cash(user_id=seller.user_id, cash=par*(best_buy_price/100))
          db.update_cash(user_id=buyer.user_id, cash=-par*(best_buy_price/100))
          print(auction.auction_id)
          del self.active_auctions[auction.auction_id]
          await asyncio.sleep(2)
          if self.active_auctions:
            continue
          else:
            break
          #print(auction.current_price)
        else:
          print("No bid has been matched")
          auction.current_price -= auction.price_step
          #await self._update_auction()
    await asyncio.sleep(3)

  async def _match_bid(self, auction_id):
    bids = [await self._process_bid(auction_id)]
    m_bids = await asyncio.gather(*bids)
    self.id_matches = [m_bid for m_bid in m_bids if m_bids is not None]
    #for bid in self.bids:
    #  if auction_id in bid:
    #    self.id_matches.append(asyncio.gather(self._process_bid(bid)))

    if self.id_matches:
      largest = heapq.nlargest(1, self.id_matches)
      best_buy_price, id, user = largest[0]
      self.id_matches.clear()
      return best_buy_price, user, id
    else:
      return None

  async def _process_bid(self, auction_id):
    for bid in self.bids:
      if auction_id in bid:
        return bid
