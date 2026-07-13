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
        
        # 1. گولڈ ریٹس (24K)
        report += "--- گولڈ ریٹس (24K) ---\n"
        rates = soup.find_all('p', class_='goldratehome')
        if len(rates) >= 3:
            report += f"1 Tola: {rates[0].text}\n10 Gram: {rates[1].text}\n1 Gram: {rates[2].text}\n\n"
        
        # 2. لائیو مارکیٹ اور شہروں کے ریٹس
        report += "--- لائیو مارکیٹ ریٹس ---\n"
        tables = soup.find_all('div', class_='progress-table')
        if len(tables) > 0:
            rows = tables[0].find_all('div', class_='table-row')
            for row in rows:
                report += row.get_text(separator=' | ', strip=True) + "\n"
        
        # 3. 15 دن کا مکمل ڈیٹا (یہاں ہم نے لمٹ ختم کر دی ہے)
        report += "\n--- گزشتہ 15 دنوں کا ٹرینڈ (مکمل تفصیل) ---\n"
        # ہسٹری ٹیبل عموماً دوسرے progress-table میں ہوتا ہے
        if len(tables) > 1:
            history_rows = tables[1].find_all('div', class_='table-row')
            for row in history_rows:
                report += row.get_text(separator=' | ', strip=True) + "\n"

        # 4. گولڈ اور سلور پوریٹی ڈیٹیلز (پیج کے اینڈ سے)
        report += "\n--- گولڈ اور سلور پوریٹی (معیار کی تفصیل) ---\n"
        # پیج کے اینڈ پر موجود text14 کلاس سے ڈیٹا
        purity_text = soup.find('div', class_='text14')
        if purity_text:
            report += purity_text.get_text(separator='\n', strip=True)

        report += "\n\nتازہ ترین اپڈیٹ: Gold.pk | Tajseed o Tajweed"
        
        send_email(report)
        print("مکمل رپورٹ بشمول پوریٹی اور 15 دن کا ڈیٹا بھیج دیا گیا ہے۔")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
