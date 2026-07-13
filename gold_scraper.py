import requests
from bs4 import BeautifulSoup
import smtplib
import os
from email.message import EmailMessage

def send_email(report):
    msg = EmailMessage()
    msg['Subject'] = "📈 مکمل گولڈ اور سلور اپڈیٹ (Gold.pk)"
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
        
        # تمام ڈیٹا کو ایک صاف رپورٹ میں جمع کرنا
        report = "📊 تازہ ترین گولڈ اور سلور ریٹس رپورٹ\n\n"
        
        # تمام ٹیبلز کو ایک ایک کر کے پڑھنا
        tables = soup.find_all('table')
        for i, table in enumerate(tables):
            report += f"\n--- سیکشن {i+1} ---\n"
            report += table.get_text(separator=' | ', strip=True)
            report += "\n"
        
        report += "\n\nسورس: https://gold.pk/"
        send_email(report)
        print("رپورٹ کامیابی سے ای میل کر دی گئی ہے۔")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
