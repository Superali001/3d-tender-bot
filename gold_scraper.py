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
        
        report = "🌟 Tajseed o Tajweed - مکمل گولڈ اور سلور رپورٹ\n"
        report += "==========================================\n\n"
        
        # 1. گولڈ ریٹس
        report += "--- گولڈ ریٹس (24K) ---\n"
        rates = soup.find_all('p', class_='goldratehome')
        if len(rates) >= 3:
            report += f"1 Tola: {rates[0].get_text()}\n10 Gram: {rates[1].get_text()}\n1 Gram: {rates[2].get_text()}\n\n"
        
        # 2. سلور ریٹس
        report += "--- سلور ریٹس ---\n"
        tables = soup.find_all('div', class_='progress-table')
        if len(tables) > 0:
            for row in tables[0].find_all('div', class_='table-row'):
                if "Silver" in row.get_text():
                    report += row.get_text(separator=' | ', strip=True) + "\n"

        # 3. 15 دن کا مکمل ٹرینڈ
        report += "\n--- گزشتہ 15 دنوں کا ٹرینڈ (مکمل) ---\n"
        history_wrap = soup.find('div', class_='progress-table-wrap')
        if history_wrap:
            report += history_wrap.get_text(separator=' ', strip=True)

        # 4. گولڈ ریٹ ٹیبل (وزن اور کیرٹ)
        report += "\n\n--- گولڈ ریٹ چارٹ (وزن اور کیرٹ) ---\n"
        gold_table = soup.find('table')
        if gold_table:
            report += gold_table.get_text(separator=' | ', strip=True)

        # 5. پوریٹی ڈیٹیلز
        report += "\n\n--- گولڈ اور سلور پوریٹی (معیار) ---\n"
        purity_text = soup.find('div', class_='text14')
        if purity_text:
            report += purity_text.get_text(separator='\n', strip=True)

        report += "\n\nتازہ ترین اپڈیٹ: Gold.pk | Tajseed o Tajweed"
        
        send_email(report)
        print("مکمل رپورٹ کامیابی سے بھیج دی گئی ہے۔")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
