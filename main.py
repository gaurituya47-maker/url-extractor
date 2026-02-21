import yfinance as yf
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def get_market_data(symbols):
    data = {}
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period='7d')
            if not hist.empty:
                data[symbol] = round(float(hist['Close'].iloc[-1]), 2)
            else:
                data[symbol] = 0
        except:
            data[symbol] = 0
    return data

def get_readawrite_stats(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
    try:
        res = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(res.text, 'lxml')
        def clean(s):
            el = soup.select_one(s)
            return el.get_text(strip=True) if el else "0"
        
        title_el = soup.find('h1')
        return {
            "title": title_el.get_text(strip=True) if title_el else "N/A",
            "views": clean('.read-count'),
            "hearts": clean('.heart-count'),
            "comments": clean('.comment-count'),
            "shelf": clean('.add-to-shelf-count')
        }
    except:
        return {"title": "Error", "views": "0", "hearts": "0", "comments": "0", "shelf": "0"}

if __name__ == "__main__":
    results = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "market": get_market_data(['BTC-USD', 'ETH-USD']),
        "novel_stats": get_readawrite_stats("https://www.readawrite.com/a/9467f5cee3135951bfbb28781edee037")
    }
    with open('dashboard_stats.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print("Done!")