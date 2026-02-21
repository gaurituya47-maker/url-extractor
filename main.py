import yfinance as yf
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# --- 1. ส่วนดึงราคาเหรียญ/หุ้น ---
def get_market_data(symbols):
    data = {}
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period='1d')
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                data[symbol] = round(float(current_price), 2)
            else:
                data[symbol] = "N/A"
        except:
            data[symbol] = "Error"
    return data

# --- 2. ส่วนดึงสถิตินิยายจาก ReadAWrite ---
def get_readawrite_stats(url):
    # สำคัญมาก: ต้องใส่ User-Agent เพื่อให้เว็บยอมให้ดึงข้อมูล
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # เจาะจงตำแหน่งสถิติของ ReadAWrite
        stats = {
            "title": soup.select_one('h1.title-name').get_text(strip=True) if soup.select_one('h1.title-name') else "N/A",
            "views": soup.select_one('span.read-count').get_text(strip=True) if soup.select_one('span.read-count') else "0",
            "hearts": soup.select_one('span.heart-count').get_text(strip=True) if soup.select_one('span.heart-count') else "0",
            "comments": soup.select_one('span.comment-count').get_text(strip=True) if soup.select_one('span.comment-count') else "0",
            "shelf": soup.select_one('span.add-to-shelf-count').get_text(strip=True) if soup.select_one('span.add-to-shelf-count') else "0"
        }
        return stats
    except Exception as e:
        return {"error": str(e)}

# --- 3. ส่วนหลักที่รันระบบ ---
if __name__ == "__main__":
    # ใส่ URL นิยายที่คุณส่งมา
    novel_url = "https://www.readawrite.com/a/9467f5cee3135951bfbb28781edee037"
    market_list = ['BTC-USD', 'ETH-USD']

    print("กำลังเริ่มดึงข้อมูล...")
    
    results = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "market": get_market_data(market_list),
        "novel_stats": get_readawrite_stats(novel_url)
    }

    # บันทึกข้อมูลลง JSON
    with open('dashboard_stats.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    
    print("อัปเดตข้อมูลลง dashboard_stats.json เรียบร้อยแล้ว!")