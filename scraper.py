import requests
from bs4 import BeautifulSoup
import smtplib
import os
from email.message import EmailMessage

# 1. ویب سائٹس کی لسٹ
targets = [
    {"url": "https://epms.ppra.gov.pk/public/tenders/active-tenders", "name": "PPRA_Federal"},
    {"url": "https://ppra.punjab.gov.pk/tenders", "name": "PPRA_Punjab"},
    {"url": "https://epads.punjab.gov.pk/open-opportunities/", "name": "EPADS_Punjab"},
    {"url": "https://www.pitb.gov.pk/tenders", "name": "PITB_Tenders"}
]

# 2. آپ کے کام کے مطابق کی ورڈز
keywords = [
    "3d modeling", "3d printing", "cad cam", "industrial design", 
    "cnc", "prototyping", "3d scanner", "digital design"
]

# 3. ای میل بھیجنے کا فنکشن
def send_email(keyword, site_name, url):
    msg = EmailMessage()
    msg['Subject'] = f"Alert: New 3D Design Tender - {keyword}"
    msg['From'] = "superali001@gmail.com"
    msg['To'] = "superali001@gmail.com"
    msg.set_content(f"توجہ فرمائیں! نیا ٹینڈر ملا ہے:\n\nکی ورڈ: {keyword}\nویب سائٹ: {site_name}\nلنک: {url}")
    
    # GitHub Secret سے پاس ورڈ لے رہا ہے
    password = os.environ.get('EMAIL_PASSWORD')
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login("superali001@gmail.com", password)
        smtp.send_message(msg)

# 4. مین سکریپنگ لوپ
for target in targets:
    try:
        response = requests.get(target["url"], timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text().lower()
        
        for k in keywords:
            if k in text:
                send_email(k, target['name'], target['url'])
    except Exception as e:
        print(f"Error checking {target['name']}: {e}")