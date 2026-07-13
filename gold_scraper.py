import requests
from bs4 import BeautifulSoup
import smtplib
import os
import logging
from email.message import EmailMessage

# لاگنگ کنفیگریشن
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_html_content(url):
    """ویب سائٹ سے ڈیٹا حاصل کرنا"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    with requests.Session() as session:
        response = session.get(url, headers=headers, timeout=30)
        response.raise_for_status() 
        return response.text

def parse_market_data(html):
    """ڈیٹا کو صاف کرنا اور صرف مطلوبہ ٹیبلز نکالنا"""
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('div', class_='progress-table')
    history_wrap = soup.find('div', class_='progress-table-wrap')
    return tables[0] if tables else None, history_wrap

def generate_email_body(live_table, history_table):
    """HTML ای میل باڈی تیار کرنا"""
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: sans-serif; color: #333; }}
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
            th {{ background: #f4f4f4; padding: 10px; text-align: left; border: 1px solid #ddd; }}
            td {{ padding: 10px; border: 1px solid #ddd; }}
            h2 {{ color: #d4af37; border-bottom: 2px solid #d4af37; padding-bottom: 5px; }}
            .purity-box {{ background-color: #f9f9f9; padding: 15px; border: 1px solid #ddd; border-radius: 5px; margin-top: 20px; font-size: 14px; }}
            .purity-box h3 {{ margin-top: 0; color: #333; }}
            .purity-box ul {{ list-style-type: none; padding-left: 0; }}
            .purity-box li {{ margin-bottom: 5px; }}
        </style>
    </head>
    <body>
        <h2>🌟 Tajseed o Tajweed - مارکیٹ اپڈیٹ</h2>
    """
    
    # 1. لائیو ریٹس
    if live_table:
        html += "<h3>شہروں کے لائیو ریٹس</h3><table>"
        for row in live_table.find_all('div', class_='table-row'):
            cols = [div.get_text(strip=True) for div in row.find_all('div', recursive=False)]
            if cols and "Top City" not in cols[0]:
                html += f"<tr><td>{'</td><td>'.join(cols[:4])}</td></tr>"
        html += "</table>"
    

    # 3. سلور / گولڈ پوریٹی ڈیٹیلز
    html += """
    <div class="purity-box">
        <h3>Silver / Gold Purity Details</h3>
        <ul>
            <li>> 24 Karat Gold is called Gold 999 and it 99.99% pure</li>
            <li>> 22 Karat Gold is called Gold 916 and it 91.67% pure.</li>
            <li>> 21 Karat Gold is called Gold 875 and it 87.50% pure.</li>
            <li>> 20 Karat Gold is called Gold 833 and it 83.33% pure.</li>
            <li>> 18 Karat Gold is called Gold 750 and it 75.00% pure.</li>
            <li>> 16 Karat Gold is called Gold 667 and it 66.67% pure.</li>
            <li>> 14 Karat Gold is called Gold 583 and it 58.33% pure.</li>
            <li>> 12 Karat Gold is called Gold 500 and it 50.00% pure.</li>
            <li>> 10 Karat Gold is called Gold 417 and it 41.67% pure.</li>
            <li>> Silver fine is 99.99% pure, also called Silver 999 or 24K</li>
            <li>> Silver Sterling is 92.5% pure, also called Silver 925 or 22K</li>
            <li>> Silver Coin is 90.00% pure, also called Silver 900 or 21K</li>
            <li>> Silver German is 80.00% pure, also called Silver 800</li>
        </ul>
    </div>
    """
        
    html += "</body></html>"
    return html

def send_email(html_content):
    """ای میل بھیجنے کا فنکشن"""
    msg = EmailMessage()
    msg['Subject'] = "📊 Tajseed o Tajweed - مارکیٹ رپورٹ"
    msg['From'] = "superali001@gmail.com"
    msg['To'] = "superali001@gmail.com"
    msg.add_alternative(html_content, subtype='html')
    
    password = os.environ.get('EMAIL_PASSWORD')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login("superali001@gmail.com", password)
        smtp.send_message(msg)

def run():
    try:
        logging.info("اسکریپنگ شروع ہو رہی ہے...")
        html = get_html_content("https://gold.pk/")
        live, history = parse_market_data(html)
        email_body = generate_email_body(live, history)
        send_email(email_body)
        logging.info("رپورٹ کامیابی سے بھیج دی گئی ہے۔")
    except Exception as e:
        logging.error(f"ایرر: {e}")

if __name__ == "__main__":
    run()
