import requests
from bs4 import BeautifulSoup
import smtplib
import os
from email.message import EmailMessage

def send_email(report):
    msg = EmailMessage()
    msg['Subject'] = "📈 Gold & Market Rates Update (Gold.pk)"
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
        
        # Gold.pk کا ڈیٹا ڈھونڈنا
        report = "📊 گولڈ اور مارکیٹ ریٹس اپڈیٹ (Gold.pk):\n\n"
        
        # ویب سائٹ کے ٹیبلز سے ڈیٹا نکالنا
        for table in soup.find_all('table'):
            for row in table.find_all('tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    key = cols[0].get_text(strip=True)
                    value = cols[1].get_text(strip=True)
                    report += f"• {key}: {value}\n"
        
        report += "\nسورس: https://gold.pk/"
        
        if len(report) > 100:
            send_email(report)
            print("ڈیٹا کامیابی سے ای میل کر دیا گیا ہے۔")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
