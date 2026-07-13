import requests
from bs4 import BeautifulSoup
import smtplib
import os
from email.message import EmailMessage

def send_email(report):
    msg = EmailMessage()
    msg['Subject'] = "📊 Tajseed o Tajweed - مکمل مارکیٹ رپورٹ"
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
        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        report = "🌟 Tajseed o Tajweed - مکمل مارکیٹ رپورٹ\n"
        report += "==========================================\n\n"
        
        # 1. گولڈ ریٹ چارٹ (وزن اور کیرٹ)
        report += "--- گولڈ ریٹ چارٹ (وزن اور کیرٹ) ---\n"
        gold_table = soup.find('table')
        if gold_table:
            # اب ہر سیل کے بعد ایک نئی لائن آئے گی تاکہ ڈیٹا بکھر نہ جائے
            report += gold_table.get_text(separator='\t', strip=True) + "\n\n"
        
        # 2. 15 دن کا ٹرینڈ (ٹیبل فارمیٹ میں)
        report += "--- گزشتہ 15 دنوں کا ٹرینڈ ---\n"
        history_wrap = soup.find('div', class_='progress-table-wrap')
        if history_wrap:
            rows = history_wrap.find_all('div', class_='table-row')
            for row in rows:
                # ہر کالم کے درمیان ایک ٹیب (Tab) کا فاصلہ
                report += row.get_text(separator='\t', strip=True) + "\n"

        # 3. پوریٹی ڈیٹیلز
        report += "\n--- سلور اور گولڈ پوریٹی (معیار) ---\n"
        purity_div = soup.find('div', class_='text14')
        if purity_div:
            # یہاں بھی ہر پوائنٹ الگ لائن میں آئے گا
            report += purity_div.get_text(separator='\n', strip=True)

        report += "\n\nتازہ ترین اپڈیٹ: Gold.pk | Tajseed o Tajweed"
        
        send_email(report)
        print("رپورٹ کامیابی سے بھیج دی گئی ہے۔")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
