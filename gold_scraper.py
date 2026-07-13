import requests
from bs4 import BeautifulSoup
import smtplib
import os
from email.message import EmailMessage

def run():
    session = requests.Session()
    # ایک مکمل کروم براؤزر کے ہیڈرز
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Referer': 'https://www.google.com/'
    }
    
    try:
        # پہلے ہوم پیج کو وزٹ کریں تاکہ کوکیز سیٹ ہوں
        session.get('https://gold.pk/', headers=headers)
        # پھر ڈیٹا حاصل کریں
        response = session.get('https://gold.pk/', headers=headers, timeout=30)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # تلاش کریں کہ کیا واقعی ٹیکسٹ موجود ہے
        print(f"Content length: {len(response.text)}")
        
        # اگر اب بھی خالی ہے، تو مجھے بتائیں، ہم ایک اور "ڈائریکٹ" لنک ٹرائی کریں گے۔
        # یہاں وہ سارا پرانا لاجک لکھیں جو ہم نے ٹیبل نکالنے کے لیے بنایا تھا
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
