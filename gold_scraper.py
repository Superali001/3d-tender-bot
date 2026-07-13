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
    
    # ای میل کو HTML فارمیٹ میں سیٹ کرنے کے لیے
    msg.add_alternative(html_report, subtype='html')
    
    password = os.environ.get('EMAIL_PASSWORD')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login("superali001@gmail.com", password)
        smtp.send_message(msg)

def run():
    url = "https://gold.pk/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # HTML اور CSS ڈیزائن کی شروعات (پروفیشنل گولڈ اینڈ گرے تھیم)
        html_content = """
        <html>
        <head>
        <style>
            body { font-family: 'Segoe UI', Arial, sans-serif; margin: 20px; color: #333; background-color: #f4f4f6; }
            .container { max-width: 850px; margin: auto; background: #fff; padding: 25px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-top: 6px solid #d4af37; }
            .header { text-align: center; padding-bottom: 20px; border-bottom: 2px solid #f1f1f1; }
            .header h1 { color: #d4af37; margin: 0; font-size: 26px; }
            .header p { color: #777; margin: 5px 0 0 0; font-size: 14px; }
            h2 { color: #333; border-bottom: 2px solid #d4af37; padding-bottom: 5px; font-size: 18px; margin-top: 30px; text-transform: uppercase; }
            table { width: 100%; border-collapse: collapse; margin-top: 10px; margin-bottom: 20px; font-size: 14px; background: #fff; }
            th, td { border: 1px solid #e0e0e0; padding: 12px 10px; text-align: left; }
            th { background-color: #f8f9fa; color: #555; font-weight: 600; text-transform: capitalize; }
            tr:nth-child(even) { background-color: #fafafa; }
            tr:hover { background-color: #f1f1f1; }
            .purity-box { background: #fffdf5; border-left: 4px solid #d4af37; padding: 15px; border-radius: 4px; font-size: 13px; line-height: 1.8; color: #444; margin-top: 10px; }
            .footer { text-align: center; margin-top: 40px; font-size: 12px; color: #999; border-top: 1px solid #eee; padding-top: 20px; }
        </style>
        </head>
        <body>
        <div class="container">
            <div class="header">
                <h1>🌟 Tajseed o Tajweed</h1>
                <p>روزانہ لائیو گولڈ اور سلور مارکیٹ رپورٹ</p>
            </div>
        """
        
        # 1. بڑے شہروں کے لائیو ریٹس (Today Gold Prices in Major Cities)
        html_content += "<h2>1. شہروں کے لائیو گولڈ ریٹس (Major Cities)</h2>"
        html_content += "<table><tr><th>Top City</th><th>Symbol</th><th>Bidding</th><th>Asking</th></tr>"
        tables = soup.find_all('div', class_='progress-table')
        if len(tables) > 0:
            rows = tables[0].find_all('div', class_='table-row')
            for row in rows:
                cols = [div.get_text(strip=True) for div in row.find_all('div', recursive=False)]
                if cols and "Top City" not in cols[0]:
                    # شہر کے ریٹس کی پہلی 4 ویلیوز شامل کریں
                    html_content += "<tr>"
                    for col in cols[:4]:
                        html_content += f"<td>{col}</td>"
                    html_content += "</tr>"
        html_content += "</table>"
        
        # 2. وزن اور کیرٹ کا مین ٹیبل (Gold Price in Pakistan Table)
        html_content += "<h2>2. گولڈ ریٹس بلحاظ وزن اور کیرٹ (Weightage & Karat)</h2>"
        html_content += "<table>"
        gold_table = soup.find('table')
        if gold_table:
            for row in gold_table.find_all('tr'):
                html_content += "<tr>"
                cells = row.find_all(['th', 'td'])
                for cell in cells:
                    tag = "th" if cell.name == "th" else "td"
                    html_content += f"<{tag}>{cell.get_text(strip=True)}</{tag}>"
                html_content += "</tr>"
        html_content += "</table>"
        
        # 3. گزشتہ 15 دن کا مکمل ہسٹری ٹرینڈ چارٹ
        html_content += "<h2>3. گزشتہ 15 دنوں کا مارکیٹ ٹرینڈ (Historical Trend)</h2>"
        html_content += "<table><tr><th>Date</th><th>Closing Rate</th><th>Day High</th><th>Day Low</th></tr>"
        history_wrap = soup.find('div', class_='progress-table-wrap')
        target_history = history_wrap if history_wrap else (tables[1] if len(tables) > 1 else None)
        if target_history:
            history_rows = target_history.find_all('div', class_='table-row')
            for row in history_rows:
                cols = [div.get_text(strip=True) for div in row.find_all('div', recursive=False)]
                if cols and "Date" not in cols[0]:
                    html_content += "<tr>"
                    for col in cols[:4]:
                        html_content += f"<td>{col}</td>"
                    html_content += "</tr>"
        html_content += "</table>"

        # 4. سلور اور گولڈ پوریٹی ڈیٹیلز
        html_content += "<h2>4. سلور اور گولڈ پوریٹی گائیڈ (Purity Details)</h2>"
        purity_div = soup.find('div', class_='text14')
        if purity_div:
            purity_text = purity_div.get_text(separator='<br>', strip=True)
            html_content += f"<div class='purity-box'>{purity_text}</div>"

        # فوٹر کا اختتام
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
        print("کامیابی: مکمل رپورٹ HTML فارمیٹ میں ای میل کر دی گئی ہے۔")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
