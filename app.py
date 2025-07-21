from flask import Flask, request, jsonify
from pytrends.request import TrendReq
import time

app = Flask(__name__)
pytrends = TrendReq(hl='en-US', tz=360)

@app.route('/trend', methods=['GET'])
def get_trend():
    keywords = request.args.getlist('keyword')  # Now supports ?keyword[]=A&keyword[]=B...

    if not keywords:
        return jsonify({"error": "No keyword(s) provided"}), 400

    results = []

    try:
        for keyword in keywords:
            time.sleep(1.5)  # Conservative delay to avoid Google Trends rate limits

            pytrends.build_payload([keyword], cat=0, timeframe='today 3-m', geo='', gprop='')
            data = pytrends.interest_over_time()

            if data.empty:
                results.append({"keyword": keyword, "error": "No data"})
            else:
                trend_data = {
                    str(k): int(v) for k, v in data[keyword].dropna().items()
                }
                results.append({"keyword": keyword, "trend": trend_data})

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
