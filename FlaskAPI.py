app = Flask(__name__)

@app.route("/add_user", methods=['POST'])
def add_user():
  data = request.get_json()
  user_id = data['user_id']
  portfolio = data['portfolio']
  engine.add_user(user_id=user_id, portfolio=portfolio)
  return jsonify({'user_id': user_id, 'portfolio': portfolio})

@app.route("/add_order", methods=['POST'])
def add_order():
  data = request.get_json()
  user_id = data['user_id']
  order_type = data['order_type']
  par = data['par']
  cusip = data['cusip']
  price = data['price']
  side = data['side']
  engine.add_order(user_id=user_id, order_type=order_type, par=par, cusip=cusip, price=price, side=side)
  return jsonify({'user_id': user_id, 'order_type': order_type, 'par': par, 'cusip': cusip, 'price': price, 'side': side})


@app.route("/create_auction", methods=['POST'])
def create_auction():
  data = request.get_json()
  user_id = data['user_id']
  cusip = data['cusip']
  par = data['par']
  start_price = data['start_price']
  reserve_price = data['reserve_price']
  price_step = data['price_step']
  current_price = data['current_price']
  timestep = data['timestep']
  ma.create_auction(user_id=user_id, cusi=cusip, par=par, start_price=start_price, reserve_price=reserve_price, price_step=price_step, current_price=current_price, timestep=timestep)
  return jsonify({'user_id': user_id, 'cusip': cusip, 'par': par, 'start_price': start_price, 'reserve_price': reserve_price, 'price_step': price_step, 'current_price': current_price, 'timestep': timestep})


@app.route("place_bid", methods=["POST"])
def place_bid():
  data = request.get_json()
  user_id = data['user_id']
  auction_id = data['auction_id']
  price = data['price']
  ma.place_bid(user_id=user_id, auction_id=auction_id, price=price)
  return jsonify({'user_id': user_id, 'auction_id': auction_id, 'price': price})
