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
        # پورے پیج کے ٹیکسٹ کو صاف کر کے نکالیں
        text = response.text
        
        # اگر آپ صرف لاہور کا ریٹ چاہتے ہیں تو یہ طریقہ سب سے بہترین ہے
        report = "📊 Gold Rates Update (Gold.pk):\n\n"
        
        # ہم ویب سائٹ کے 'Today Gold Prices' والے سیکشن کو ٹارگٹ کریں گے
        import re
        # یہ ریگولر ایکسپریشن (Regex) سیدھے ریٹس اٹھائے گی
        rates = re.findall(r"Gold Rate in Lahore.*?Rs\.\s*([\d,]+)", text, re.DOTALL)
        
        if rates:
            report += f"• Lahore Gold Rate: Rs. {rates[0]}"
            send_email(report)
            print("ریٹ کامیابی سے ای میل کر دیے گئے ہیں۔")
        else:
            print("ریٹس نہیں مل سکے۔")
            
    except Exception as e:
        print(f"Error: {e}")
