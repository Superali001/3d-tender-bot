import requests
from bs4 import BeautifulSoup
import smtplib
import os
from email.message import EmailMessage

def send_email(html_report):
    msg = EmailMessage()
    msg['Subject'] = "📊 Tajseed o Tajweed - مکمل مارکیٹ رپورٹ"
    msg['From'] = "superali001@gmail.com"
    msg['To'] = "superali001@gmail.com"
    
    msg.add_alternative(html_report, subtype='html')
    
    password = os.environ.get('EMAIL_PASSWORD')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login("superali001@gmail.com", password)
        smtp.send_message(msg)

def run():
    url = "https://gold.pk/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # پریمیم بزنس لک کے لیے CSS اسٹائلنگ
        html_content = """
        <html>
        <head>
        <style>
            body { font-family: 'Segoe UI', Arial, sans-serif; background-color: #f4f6f9; margin: 0; padding: 20px; }
            .wrapper { max-width: 850px; margin: auto; background: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); border-top: 6px solid #d4af37; }
            .brand-header { text-align: center; border-bottom: 2px solid #f1f1f1; padding-bottom: 15px; margin-bottom: 25px; }
            .brand-header h1 { color: #d4af37; margin: 0; font-size: 28px; font-weight: 700; letter-spacing: 1px; }
            .brand-header p { color: #666; margin: 5px 0 0 0; font-size: 14px; }
            h2 { color: #2c3e50; font-size: 16px; border-left: 4px solid #d4af37; padding-left: 10px; margin-top: 35px; margin-bottom: 15px; text-transform: uppercase; }
            table { width: 100%; border-collapse: collapse; margin-bottom: 25px; font-size: 14px; }
            th { background-color: #f8f9fa; color: #333; font-weight: 600; text-align: left; border: 1px solid #e9ecef; padding: 12px 10px; }
            td { border: 1px solid #e9ecef; padding: 12px 10px; text-align: left; color: #495057; }
            tr:nth-child(even) { background-color: #fafafa; }
            .purity-box { background-color: #fffdf6; border: 1px solid #f4ecd0; padding: 15px; border-radius: 6px; font-size: 13px; color: #555; }
            .purity-box ul { margin: 0; padding-left: 20px; }
            .purity-box li { margin-bottom: 5px; }
            .footer { text-align: center; border-top: 1px solid #eee; padding-top: 15px; margin-top: 35px; font-size: 12px; color: #999; }
        </style>
        </head>
        <body>
        <div class="wrapper">
            <div class="brand-header">
                <h1>🌟 TAJSEED O TAJWEED</h1>
                <p>روزانہ لائیو گولڈ اور سلور مارکیٹ رپورٹ</p>
            </div>
        """

        # 1. شہروں کے لائیو ریٹس
        html_content += "<h2>1. شہروں کے لائیو گولڈ ریٹس (Major Cities)</h2>"
        html_content += "<table><thead><tr><th>Lahore City</th><th>Symbol</th><th>Bidding</th><th>Asking</th></tr></thead><tbody>"
        
        tables = soup.find_all('div', class_='progress-table')
        if tables:
            city_rows = tables[0].find_all('div', class_='table-row')
            for row in city_rows:
                cols = [div.get_text(strip=True) for div in row.find_all('div', recursive=False)]
                if not cols or "Top City" in cols[0] or "Gold Rates" in cols[0] or "XAUP" in "".join(cols):
                    continue
                if len(cols) >= 4:
                    html_content += f"<tr><td>{cols[0]}</td><td>{cols[1]}</td><td>{cols[2]}</td><td>{cols[3]}</td></tr>"
        html_content += "</tbody></table>"

        # 2. گزشتہ 15 دن کا ٹرینڈ
        html_content += "<h2>2. گزشتہ 15 دنوں کا مارکیٹ ٹرینڈ (Daily Gold Rates)</h2>"
        html_content += "<table><thead><tr><th>Date</th><th>Closing Rate</th><th>Day High</th><th>Day Low</th></tr></thead><tbody>"
        
        history_wrap = soup.find('div', class_='progress-table-wrap')
        target_history = history_wrap if history_wrap else (tables[1] if len(tables) > 1 else None)
        
        if target_history:
            history_rows = target_history.find_all('div', class_='table-row')
            for row in history_rows:
                cols = [div.get_text(strip=True) for div in row.find_all('div', recursive=False)]
                if not cols or "Date" in cols[0] or "Gold Rates" in cols[0] or "XAUP" in "".join(cols):
                    continue
                if len(cols) >= 4:
                    html_content += f"<tr><td>{cols[0]}</td><td>{cols[1]}</td><td>{cols[2]}</td><td>{cols[3]}</td></tr>"
        html_content += "</tbody></table>"

        # 3. سلور اور گولڈ پوریٹی ڈیٹیلز
        html_content += "<h2>3. Silver / Gold Purity Details</h2>"
        html_content += """
        <div class="purity-box">
            <ul>
                <li>24 Karat Gold is called Gold 999 and it 99.99% pure</li>
                <li>22 Karat Gold is called Gold 916 and it 91.67% pure.</li>
                <li>21 Karat Gold is called Gold 875 and it 87.50% pure.</li>
                <li>20 Karat Gold is called Gold 833 and it 83.33% pure.</li>
                <li>18 Karat Gold is called Gold 750 and it 75.00% pure.</li>
                <li>16 Karat Gold is called Gold 667 and it 66.67% pure.</li>
                <li>14 Karat Gold is called Gold 583 and it 58.33% pure.</li>
                <li>12 Karat Gold is called Gold 500 and it 50.00% pure.</li>
                <li>10 Karat Gold is called Gold 417 and it 41.67% pure.</li>
                <li>Silver fine is 99.99% pure, also called Silver 999 or 24K</li>
                <li>Silver Sterling is 92.5% pure, also called Silver 925 or 22K</li>
                <li>Silver Coin is 90.00% pure, also called Silver 900 or 21K</li>
                <li>Silver German is 80.00% pure, also called Silver 800</li>
            </ul>
        </div>
        """

        # فوٹر
        html_content += """
            <div class="footer">
                <p>یہ رپورٹ خودکار نظام کے تحت تیار کی گئی ہے۔ ڈیٹا کا ماخذ: Gold.pk</p>
                <p>&copy; 2026 Tajseed o Tajweed. All Rights Reserved.</p>
            </div>
        </div>
        </body>
        </html>
        """
        
        send_email(html_content)
        print("کامیابی: پوریٹی ڈیٹیلز کے ساتھ رپورٹ بھیج دی گئی ہے۔")
            
    except Exception as e:
        print(f"Error processing layout: {e}")

if __name__ == "__main__":
    run()
