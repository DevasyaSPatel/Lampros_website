from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# Fallback crypto prices in case CoinGecko rate limits us
FALLBACK_PRICES = {
    "bitcoin": {"usd": 65000, "usd_24h_change": 2.5},
    "ethereum": {"usd": 3500, "usd_24h_change": 1.2},
    "solana": {"usd": 150, "usd_24h_change": -3.5},
    "matic-network": {"usd": 0.85, "usd_24h_change": 0.5}
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/concepts')
def concepts():
    return render_template('concepts.html')

@app.route('/prices')
def prices_page():
    return render_template('prices.html')

@app.route('/simulator')
def simulator():
    return render_template('simulator.html')

@app.route('/api/prices')
def api_prices():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum,bitcoin,solana,matic-network&vs_currencies=usd&include_24hr_change=true"
    headers = {
        # Using a typical browser User-Agent helps bypass some basic CDN checks
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            print(f"CoinGecko Error {response.status_code}. Using fallback data.")
            return jsonify(FALLBACK_PRICES)
    except Exception as e:
        print(f"Fetch failed: {e}. Using fallback data.")
        return jsonify(FALLBACK_PRICES)

if __name__ == '__main__':
    # Run the Flask app on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
