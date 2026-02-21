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
            hist = ticker.history(period='1d')
            current_price = hist['Close'].iloc[-1]
            data[symbol] = round(float(current_price), 2)
        except:
            data[symbol] = 0
    return data

def get_readawrite_stats(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'th-TH,th;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # ค้นหาชื่อเรื่อง
        title = soup.find('h1', class_='title-name') or soup.find('h1')
        
        # ฟังก์ชันช่วยดึงตัวเลขจาก Class ต่างๆ
        def extract_num(selector):
            el = soup.select_one(selector)
            return el.get_text(strip=True) if el else "0"

        stats = {
            "title": title.get_text(strip=True) if title else "รัชทายาทผ้าพันแผล",
            "views": extract_num('.read-count'),
            "hearts": extract_num('.heart-count'),
            "comments": extract_num('.comment-count'),
            "shelf": extract_num('.add-to-shelf-count')
        }
        
        # Debug: พิมพ์ออกหน้า Log ของ GitHub เพื่อเช็คว่าดึงได้ไหม
        print(f"ดึงข้อมูลสำเร็จ: {stats}")
        return stats
    except Exception as e:
        print(f"Error Scraper: {e}")
        return {"title": "Error", "views": "0", "hearts": "0", "comments": "0", "shelf": "0"}

if __name__ == "__main__":
    url = "https://www.readawrite.com/a/9467f5cee3135951bfbb28781edee037"
    results = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "market": get_market_data(['BTC-USD', 'ETH-USD']),
        "novel_stats": get_readawrite_stats(url)
    }
    with open('dashboard_stats.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)