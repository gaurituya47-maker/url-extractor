import yfinance as yf
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# --- 1. ส่วนดึงราคาเหรียญ/หุ้น (Market Data) ---
def get_market_data(symbols):
    data = {}
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            current_price = ticker.history(period='1d')['Close'].iloc[-1]
            data[symbol] = round(float(current_price), 2)
        except Exception as e:
            data[symbol] = f"Error: {e}"
    return data

# --- 2. ส่วนดึงยอดวิว/Engagement (Web Scraping) ---
def get_web_stats(url, selectors):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        stats = {}
        for key, selector in selectors.items():
            element = soup.select_one(selector)
            stats[key] = element.get_text(strip=True) if element else "N/A"
        return stats
    except Exception as e:
        return {"error": str(e)}

# --- 3. ส่วนประมวลผลและบันทึกข้อมูล ---
if __name__ == "__main__":
    # ตั้งค่าสิ่งที่ต้องการดึง
    market_symbols = ['BTC-USD', 'ETH-USD', 'GC=F'] # BTC, ETH, GOLD
    
    # ตัวอย่าง: ดึงยอดวิวจากหน้าเว็บนิยาย (แก้ URL และ Selector ตามเว็บจริง)
    web_url = "https://example.com/your-novel" 
    web_selectors = {
        "total_views": ".view-count", 
        "likes": ".heart-count"
    }

    # เริ่มดึงข้อมูล
    print("Fetching data...")
    final_output = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "market": get_market_data(market_symbols),
        "engagement": get_web_stats(web_url, web_selectors)
    }

    # บันทึกเป็นไฟล์ JSON เพื่อให้ Dashboard เรียกใช้
    with open('dashboard_stats.json', 'w', encoding='utf-8') as f:
        json.dump(final_output, f, ensure_ascii=False, indent=4)
    
    print("Successfully updated dashboard_stats.json!")