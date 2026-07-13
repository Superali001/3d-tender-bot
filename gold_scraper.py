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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # HTML اور CSS ڈیزائن (خوبصورت رپورٹ کے لیے)
        html_content = """
        <html>
        <head>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f6f9; padding: 20px; color: #333; direction: ltr; }
            .container { max-width: 800px; margin: auto; background: #ffffff; padding: 25px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border-top: 5px solid #d4af37; }
            h1 { color: #d4af37; text-align: center; font-size: 24px; margin-bottom: 5px; }
            .subtitle { text-align: center; color: #777; font-size: 14px; margin-bottom: 30px; border-bottom: 1px solid #eee; padding-bottom: 15px; }
            h2 { color: #2c3e50; font-size: 16px; border-left: 4px solid #d4af37; padding-left: 10px; margin-top: 30px; text-transform: uppercase; }
            table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13px; }
            th, td { border: 1px solid #e9ecef; padding: 10px; text-align: left; }
            th { background-color: #f8f9fa; color: #333; font-weight: bold; }
            tr:nth-child(even) { background-color: #fdfdfd; }
            .purity-box { background-color: #fffdf6; border: 1px solid #f4ecd0; padding: 15px; border-radius: 5px; font-size: 13px; line-height: 1.8; color: #555; }
            .footer { text-align: center; margin-top: 30px; font-size: 12px; color: #999; border-top: 1px solid #eee; padding-top: 15px; }
        </style>
        </head>
        <body>
        <div class="container">
            <h1>🌟 TAJSEED O TAJWEED</h1>
            <div class="subtitle">لائیو گولڈ اور سلور مارکیٹ رپورٹ</div>
        """
        
        # 1. شہروں کے لائیو ریٹس
        html_content += "<h2>1. لائیو مارکیٹ اور شہروں کے ریٹس</h2>"
        html_content += "<table><tr><th>Top City</th><th>Symbol</th><th>Bidding</th><th>Asking</th></tr>"
        tables = soup.find_all('div', class_='progress-table')
        if len(tables) > 0:
            for row in tables[0].find_all('div', class_='table-row'):
                cols = [col.get_text(strip=True) for col in row.find_all('div', recursive=False)]
                if cols and "Top City" not in cols[0]:
                    html_content += "<tr>"
                    for col in cols[:4]:
                        html_content += f"<td>{col}</td>"
                    html_content += "</tr>"
        html_content += "</table>"
        
        # 2. گولڈ ریٹس (وزن اور کیرٹ)
        html_content += "<h2>2. گولڈ ریٹس (وزن اور کیرٹ)</h2>"
        html_content += "<table>"
        gold_table = soup.find('table')
        if gold_table:
            for row in gold_table.find_all('tr'):
                html_content += "<tr>"
                for cell in row.find_all(['th', 'td']):
                    tag = "th" if cell.name == "th" else "td"
                    html_content += f"<{tag}>{cell.get_text(strip=True)}</{tag}>"
                html_content += "</tr>"
        html_content += "</table>"
        
        # 3. گزشتہ 15 دن کا ٹرینڈ (مکمل ڈیٹا بغیر کسی کٹوتی کے)
        html_content += "<h2>3. گزشتہ 15 دنوں کا ٹرینڈ (مکمل)</h2>"
        html_content += "<table><tr><th>Date</th><th>Closing Rate</th><th>Day High</th><th>Day Low</th></tr>"
        history_wrap = soup.find('div', class_='progress-table-wrap')
        target_table = history_wrap if history_wrap else (tables[1] if len(tables) > 1 else None)
        if target_table:
            for row in target_table.find_all('div', class_='table-row'):
                cols = [col.get_text(strip=True) for col in row.find_all('div', recursive=False)]
                if cols and "Date" not in cols[0]:
                    html_content += "<tr>"
                    for col in cols[:4]:
                        html_content += f"<td>{col}</td>"
                    html_content += "</tr>"
        html_content += "</table>"

        # 4. گولڈ اور سلور پوریٹی (معیار)
        html_content += "<h2>4. سلور اور گولڈ پوریٹی گائیڈ</h2>"
        purity_div = soup.find('div', class_='text14')
        if purity_div:
            # لائن بریک کے لیے <br> کا استعمال تاکہ ہر لائن الگ نظر آئے
            purity_text = purity_div.get_text(separator='<br>', strip=True)
            html_content += f"<div class='purity-box'>{purity_text}</div>"

        # ای میل کا اختتام
        html_content += """
            <div class="footer">
                تازہ ترین اپڈیٹ: Gold.pk<br>
                &copy; 2026 Tajseed o Tajweed. All Rights Reserved.
            </div>
        </div>
        </body>
        </html>
        """
        
        send_email(html_content)
        print("HTML رپورٹ کامیابی کے ساتھ بھیج دی گئی ہے۔")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
