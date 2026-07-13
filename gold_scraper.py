import requests
from bs4 import BeautifulSoup
import smtplib
import os
import time
from email.message import EmailMessage

def send_email(subject, report):
    msg = EmailMessage()
    msg['Subject'] = subject
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
        
        report = "🌟 Tajseed o Tajweed - مکمل گولڈ مارکیٹ رپورٹ\n"
        report += "==================================================\n\n"

        # 1. گولڈ ریٹس (24K)
        report += "--- گولڈ ریٹس (24K) ---\n"
        rates = soup.find_all('p', class_='goldratehome')
        if len(rates) >= 3:
            report += f"1 Tola: {rates[0].text}\n10 Gram: {rates[1].text}\n1 Gram: {rates[2].text}\n\n"

        # 2. مارکیٹ اور 15 دن کا ٹرینڈ (ٹیبلز کو الگ الگ تلاش کرنا)
        all_tables = soup.find_all('div', class_='progress-table')
        
        # پہلا ٹیبل مارکیٹ ریٹس کا ہوتا ہے
        report += "--- مارکیٹ ریٹس (بڈنگ / آسکنگ) ---\n"
        if len(all_tables) > 0:
            rows = all_tables[0].find_all('div', class_='table-row')
            for row in rows:
                cols = row.find_all('div')
                if len(cols) >= 3:
                    report += f"{cols[0].text.strip()} | {cols[2].text.strip()} | {cols[3].text.strip()}\n"

        # 15 دن کا ٹرینڈ (یہ عموماً دوسرے یا تیسرے ٹیبل میں ہوتا ہے)
        report += "\n--- گزشتہ 15 دنوں کا ٹرینڈ ---\n"
        if len(all_tables) > 1:
            rows = all_tables[1].find_all('div', class_='table-row')
            for row in rows:
                cols = row.find_all('div')
                if len(cols) >= 3 and "Date" not in cols[0].text:
                    report += f"{cols[0].text.strip()} | {cols[1].text.strip()}\n"

        # 3. پوریٹی (معیار) کی تفصیلات
        report += "\n--- گولڈ اور سلور پوریٹی (معیار) ---\n"
        # پوریٹی کا سیکشن 'text14' کلاس میں ہے
        purity_div = soup.find('div', class_='text14')
        if purity_div:
            # ہم صرف 24K سے نیچے کا حصہ کاپی کر رہے ہیں
            text = purity_div.text
            start = text.find("24 Karat")
            if start != -1:
                report += text[start:]

        send_email("📊 Tajseed o Tajweed - ڈیلی مارکیٹ رپورٹ", report)
        print("رپورٹ کامیابی سے بھیج دی گئی ہے۔")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
