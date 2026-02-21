import yfinance as yf
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os

def get_market_data(symbols):
    data = {}
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            # แก้ปัญหาข้อมูลว่าง: ดึงย้อนหลัง 7 วันเพื่อความชัวร์
            hist = ticker.history(period='7d')
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                data[symbol] = round(float(current_price), 2)
            else:
                data[symbol] = 0
                print(f"Warning: No data for {symbol}")
        except Exception as e:
            data[symbol] = 0
            print(f"Market Error ({symbol}): {e}")
    return data

def get_readawrite_stats(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # ฟังก์ชันดึงเลขแบบไม่ยอมพัง
        def get_text(selector):
            el = soup.select_one(selector)
            return el.get_text(strip=True) if el else "0"

        # ดึงชื่อเรื่อง
        title_el = soup.find('h1')
        title_name = title_el.get_text(strip=True) if title_el else "N/A"

        return {
            "title": title_name,
            "views": get_text('.read-count'),
            "hearts": get_text('.heart-count'),
            "comments": get_text('.comment-count'),
            "shelf": get_text('.add-to-shelf-count')
        }
    except Exception as e:
        print(f"Scraper Error: {e}")
        return {"title": "Error", "views": "0", "hearts": "0", "comments": "0", "shelf": "0"}

if __name__ == "__main__":
    url = "https://www.readawrite.com/a/9467f5cee3135951bfbb28781edee037"
    
    print("Starting Scraper...")
    results = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "market": get_market_data(['BTC-USD', 'ETH-USD']),
        "novel_stats": get_readawrite_stats(url)
    }

    # บันทึกไฟล์
    with open('dashboard_stats.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    
    print("All tasks completed!")