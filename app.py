from flask import Flask, request, jsonify
from pytrends.request import TrendReq
import time

app = Flask(__name__)
pytrends = TrendReq(hl='en-US', tz=360)

@app.route('/trend', methods=['GET'])
def get_trend():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({"error": "No keyword provided"}), 400

    try:
        time.sleep(2)  # ← helps avoid Google Trends 429 rate limit

        pytrends.build_payload([keyword], cat=0, timeframe='today 3-m', geo='', gprop='')
        data = pytrends.interest_over_time()

        if data.empty:
            return jsonify({"keyword": keyword, "error": "No data"}), 404

        trend_data = data[keyword].dropna().to_dict()
        return jsonify({"keyword": keyword, "trend": trend_data})
    
    except Exception as e:
        return jsonify({"keyword": keyword, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
