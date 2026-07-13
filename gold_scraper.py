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
    
    # ای میل کو باقاعدہ پریمیم HTML فارمیٹ میں سیٹ کرنے کے لیے
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
        
        # پریمیم بزنس لک کے لیے CSS اسٹائلنگ کی تیاری
        html_content = """
        <html>
        <head>
        <style>
            body { font-family: 'Segoe UI', Arial, sans-serif; background-color: #f4f6f9; margin: 0; padding: 20px; direction: ltr; }
            .wrapper { max-width: 800px; margin: auto; background: #ffffff; padding: 25px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.06); border-top: 6px solid #d4af37; }
            .brand-header { text-align: center; border-bottom: 2px solid #f1f1f1; padding-bottom: 15px; margin-bottom: 25px; }
            .brand-header h1 { color: #d4af37; margin: 0; font-size: 28px; font-weight: 700; letter-spacing: 1px; }
            .brand-header p { color: #666; margin: 5px 0 0 0; font-size: 14px; }
            h2 { color: #2c3e50; font-size: 16px; border-left: 4px solid #d4af37; padding-left: 10px; margin-top: 30px; margin-bottom: 15px; text-transform: uppercase; }
            table { width: 100%; border-collapse: collapse; margin-bottom: 25px; font-size: 13px; }
            th { background-color: #f8f9fa; color: #333; font-weight: 600; text-align: left; border: 1px solid #e9ecef; padding: 10px; }
            td { border: 1px solid #e9ecef; padding: 10px; text-align: left; color: #495057; }
            tr:nth-child(even) { background-color: #fdfdfd; }
            .purity-section { background-color: #fffdf6; border: 1px solid #f4ecd0; border-radius: 6px; padding: 15px; font-size: 13px; line-height: 1.8; color: #514d3e; }
            .footer { text-align: center; border-top: 1px solid #eee; padding-top: 15px; margin-top: 35px; font-size: 11px; color: #999; }
        </style>
        </head>
        <body>
        <div class="wrapper">
            <div class="brand-header">
                <h1>🌟 TAJSEED O TAJWEED</h1>
                <p>لائیو گولڈ اور سلور مارکیٹ رپورٹ</p>
            </div>
        """

        # سیکشن 1: بڑے شہروں کے لائیو ریٹس (Today Gold Prices in Major Cities)
        html_content += "<h2>1. شہروں کے لائیو گولڈ ریٹس (Major Cities of Pakistan)</h2>"
        html_content += "<table><thead><tr><th>Top City</th><th>Symbol</th><th>Bidding</th><th>Asking</th></tr></thead><tbody>"
        
        tables = soup.find_all('div', class_='progress-table')
        if tables:
            city_rows = tables[0].find_all('div', class_='table-row')
            for row in city_rows:
                # صرف بنیادی کالمز حاصل کرنے کے لیے recursive=False لازمی ہے
                cols = [div.get_text(strip=True) for div in row.find_all('div', recursive=False)]
                if cols and "Top City" not in cols[0]:
                    html_content += "<tr>"
                    # یقینی بنائیں کہ صرف پہلے 4 کالمز (شہر، سمبل، بڈ، آسک) شامل ہوں
                    for col in cols[:4]:
                        html_content += f"<td>{col}</td>"
                    html_content += "</tr>"
        html_content += "</tbody></table>"

        # سیکشن 2: وزن اور کیرٹ کا مین ٹیبل (Gold Price in Pakistan)
        html_content += "<h2>2. گولڈ ریٹس بلحاظ وزن اور کیرٹ (Weightage & Karat Chart)</h2>"
        html_content += "<table>"
        native_table = soup.find('table')
        if native_table:
            for row in native_table.find_all('tr'):
                html_content += "<tr>"
                for cell in row.find_all(['th', 'td']):
                    tag = "th" if cell.name == "th" else "td"
                    html_content += f"<{tag}>{cell.get_text(strip=True)}</{tag}>"
                html_content += "</tr>"
        html_content += "</table>"

        # سیکشن 3: گزشتہ 15 دن کا مکمل ہسٹری چارٹ
        html_content += "<h2>3. گزشتہ 15 دنوں کا مارکیٹ ٹرینڈ (Daily Gold Rates)</h2>"
        html_content += "<table><thead><tr><th>Date</th><th>Closing Rate</th><th>Day High</th><th>Day Low</th></tr></thead><tbody>"
        
        history_wrap = soup.find('div', class_='progress-table-wrap')
        # اگر مخصوص ریپر نہ ملے تو متبادل کے طور پر دوسرے پروگریس ٹیبل کو ٹارگٹ کرے گا
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
        html_content += "</tbody></table>"

        # سیکشن 4: سلور اور گولڈ پوریٹی ڈیٹیلز
        html_content += "<h2>4. سلور اور گولڈ پوریٹی گائیڈ (Purity Details)</h2>"
        purity_div = soup.find('div', class_='text14')
        if purity_div:
            # فارمیٹنگ برقرار رکھنے کے لیے ہر لائن بریک کو <br> میں تبدیل کیا گیا ہے
            purity_text = purity_div.get_text(separator='<br>', strip=True)
            html_content += f"<div class='purity-section'>{purity_text}</div>"

        # ای میل فوٹر کا اختتام
        html_content += """
            <div class="footer">
                <p>یہ رپورٹ مینوئل مداخلت کے بغیر خودکار سکریپر کے ذریعے تیار کی گئی ہے۔ ڈیٹا سورس: Gold.pk</p>
                <p>&copy; 2026 Tajseed o Tajweed. All Rights Reserved.</p>
            </div>
        </div>
        </body>
        </html>
        """
        
        # ای میل بھیجیں
        send_email(html_content)
        print("Success: Complete live data converted to HTML tables and sent successfully.")
            
    except Exception as e:
        print(f"Error processing layout: {e}")

if __name__ == "__main__":
    run()
