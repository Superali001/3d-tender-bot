import requests
from bs4 import BeautifulSoup
import smtplib
import os
from email.message import EmailMessage

def send_email(report):
    msg = EmailMessage()
    msg['Subject'] = "📈 Gold Rate Data (Debug Mode)"
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
        
        # اس بار ہم تلاش نہیں کر رہے، بلکہ تمام ٹیبلز کو ایک ایک کر کے پرنٹ کر رہے ہیں
        report = "📊 تمام ٹیبل کا ڈیٹا:\n\n"
        
        for i, table in enumerate(soup.find_all('table')):
            report += f"\n--- ٹیبل نمبر {i+1} ---\n"
            report += table.get_text(separator=' ', strip=True)
        
        send_email(report)
        print("ڈیٹا پرنٹ ہو گیا ہے، اپنی ای میل چیک کریں۔")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
