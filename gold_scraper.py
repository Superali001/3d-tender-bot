import requests
from bs4 import BeautifulSoup
import smtplib
import os
from email.message import EmailMessage

def send_email(report):
    msg = EmailMessage()
    msg['Subject'] = "📊 Tajseed o Tajweed - تازہ ترین گولڈ مارکیٹ رپورٹ"
    msg['From'] = "superali001@gmail.com"
    msg['To'] = "superali001@gmail.com"
    msg.set_content(report)
    password = os.environ.get('EMAIL_PASSWORD')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login("superali001@gmail.com", password)
        smtp.send_message(msg)

def run():
    url = "https://gold.pk/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        report = "🌟 Tajseed o Tajweed - لائیو مارکیٹ اپڈیٹ\n"
        report += "==================================================\n\n"
        
        # 1. شہروں کے ریٹس (لائیو ٹیبل سے)
        report += "--- بڑے شہروں کے ریٹس ---\n"
        report += f"{'شہر':<12} | {'بڈنگ':<10} | {'آسکنگ':<10}\n"
        report += "-" * 35 + "\n"
        
        # ویب سائٹ کے ٹیبل کو تلاش کرنا اور ریٹس نکالنا
        table = soup.find('div', class_='progress-table')
        if table:
            rows = table.find_all('div', class_='table-row')
            for row in rows:
                cols = row.find_all('div', class_='serial') # ویب سائٹ کے مطابق
                # اگر ڈیٹا مل جائے تو رپورٹ میں شامل کریں
                text = row.get_text(separator=' | ', strip=True)
                report += text + "\n"
        
        # 2. 15 دن کا ہسٹری ڈیٹا (ٹیبل سے)
        report += "\n--- گزشتہ 15 دنوں کا ٹرینڈ ---\n"
        history_table = soup.find('div', class_='progress-table-wrap')
        if history_table:
            # ٹیبل کا سارا ٹیکسٹ اٹھا لیں جو لائیو ہے
            report += history_table.get_text(separator=' ', strip=True)
            
        report += "\n\nمزید تفصیلات کے لیے ویب سائٹ وزٹ کریں۔"
        
        send_email(report)
        print("لائیو ڈیٹا کامیابی سے بھیج دیا گیا ہے۔")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
