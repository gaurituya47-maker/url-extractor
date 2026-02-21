import yfinance as yf
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def get_market_data(symbols):
    data = {}
    for symbol in symbols:
        try:
            print(f"กำลังดึงราคา: {symbol}...")
            ticker = yf.Ticker(symbol)
            # ดึงข้อมูลย้อนหลัง 5 วันเพื่อป้องกันกรณีตลาดปิดวันหยุด
            hist = ticker.history(period='5d')
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                data[symbol] = round(float(current_price), 2)
                print(f"สำเร็จ: {symbol} = {data[symbol]}")
            else:
                data[symbol] = 0
                print(f"เตือน: ไม่พบข้อมูล {symbol}")
        except Exception as e:
            data[symbol] = 0
            print(f"Error ตลาด ({symbol}): {e}")
    return data

def get_readawrite_stats(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }
    try:
        print(f"กำลังดึงข้อมูลจาก ReadAWrite...")
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        def safe_extract(selector):
            el = soup.select_one(selector)
            return el.get_text(strip=True) if el else "0"

        title_el = soup.find('h1')
        title = title_el.get_text(strip=True) if title_el else "N/A"

        stats = {
            "title": title,
            "views": safe_extract('.read-count'),
            "hearts": safe_extract('.heart-count'),
            "comments": safe_extract('.comment-count'),
            "shelf": safe_extract('.add-to-shelf-count')
        }
        print(f"ดึงข้อมูลนิยายสำเร็จ: {stats['title']}")
        return stats
    except Exception as e:
        print(f"Error ReadAWrite: {e}")
        return {"title": "Error", "views": "0", "hearts": "0", "comments": "0", "shelf": "0"}

if __name__ == "__main__":
    url = "https://www.readawrite.com/a/9467f5cee3135951bfbb28781edee037"
    print("--- เริ่มทำงาน ---")
    
    results = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "market": get_market_data(['BTC-USD', 'ETH-USD']),
        "novel_stats": get_readawrite_stats(url)
    }

    with open('dashboard_stats.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    
    print("--- จบการทำงานแบบสมบูรณ์ ---")