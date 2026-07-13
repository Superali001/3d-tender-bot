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
        
        # 1. گولڈ ریٹس کا مین ٹیبل (تصویر والا پہلا حصہ)
        report += "--- گولڈ ریٹس (وزن اور کیرٹ) ---\n"
        main_table = soup.find('table')
        if main_table:
            report += main_table.get_text(separator=' | ', strip=True) + "\n\n"
        
        # 2. 15 دن کا مکمل ٹرینڈ
        report += "--- گزشتہ 15 دن کا ٹرینڈ (مکمل) ---\n"
        history_wrap = soup.find('div', class_='progress-table-wrap')
        if history_wrap:
            report += history_wrap.get_text(separator=' ', strip=True) + "\n\n"

        # 3. سلور اور گولڈ پوریٹی ڈیٹیلز (تصویر کا آخری حصہ)
        report += "--- سلور اور گولڈ پوریٹی (معیار) ---\n"
        purity_div = soup.find('div', class_='text14')
        if purity_div:
            report += purity_div.get_text(separator='\n', strip=True)

        report += "\n\nتازہ ترین اپڈیٹ: Gold.pk | Tajseed o Tajweed"
        
        send_email(report)
        print("مکمل رپورٹ کامیابی سے بھیج دی گئی ہے۔")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
