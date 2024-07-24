from flask import Flask, request, jsonify, render_template
import requests

# Replace with your Alpha Vantage API key
ALPHA_VANTAGE_API_KEY = 'G3JOHI3MFK9V0KMS'

app = Flask(__name__)

# Dictionary to store tracked stocks
tracked_stocks = {}

def get_stock_price(symbol):
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(url)
    data = response.json()
    
    if 'Global Quote' in data and '05. price' in data['Global Quote']:
        return float(data['Global Quote']['05. price'])
    else:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_stock', methods=['POST'])
def add_stock():
    data = request.json
    symbol = data.get('symbol').upper()
    if symbol not in tracked_stocks:
        tracked_stocks[symbol] = get_stock_price(symbol)
        return jsonify({'message': f'Stock {symbol} added.', 'tracked_stocks': tracked_stocks}), 200
    else:
        return jsonify({'error': f'Stock {symbol} is already being tracked.'}), 400

@app.route('/remove_stock', methods=['POST'])
def remove_stock():
    data = request.json
    symbol = data.get('symbol').upper()
    if symbol in tracked_stocks:
        del tracked_stocks[symbol]
        return jsonify({'message': f'Stock {symbol} removed.', 'tracked_stocks': tracked_stocks}), 200
    else:
        return jsonify({'error': f'Stock {symbol} is not being tracked.'}), 400

@app.route('/tracked_stocks', methods=['GET'])
def tracked_stocks_list():
    updated_stocks = {}
    for symbol in tracked_stocks:
        updated_stocks[symbol] = get_stock_price(symbol)
    return jsonify(updated_stocks), 200

if __name__ == '__main__':
    app.run(debug=True)
