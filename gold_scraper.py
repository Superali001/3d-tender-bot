import requests
from bs4 import BeautifulSoup
import smtplib
import os
from email.message import EmailMessage

def send_email(report):
    msg = EmailMessage()
    msg['Subject'] = "📈 Gold Rate Update (Gold.pk)"
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
        
        # ویب سائٹ کے اہم حصے کو ٹارگٹ کرنا
        report = "📊 گولڈ مارکیٹ ریٹس - تازہ ترین:\n\n"
        
        # تمام ٹیبل روز کو ڈھونڈ کر ان کا ڈیٹا نکالنا
        for row in soup.find_all('tr'):
            cols = row.find_all('td')
            if len(cols) >= 3:
                # شہر اور ریٹ کا ٹیکسٹ صاف کرنا
                city = cols[0].get_text(strip=True)
                price = cols[2].get_text(strip=True)
                if city and price and price.isdigit(): # یہ صرف وہی لائنیں لے گا جہاں قیمت موجود ہے
                    report += f"• {city}: Rs. {price}\n"
        
        # اگر رپورٹ میں ڈیٹا آیا تو بھیج دیں
        if len(report) > 50:
            send_email(report)
            print("ای میل کامیابی سے بھیج دی گئی ہے۔")
        else:
            print("ڈیٹا نہیں مل سکا، براہِ کرم چیک کریں کہ ٹیبلز صحیح لوڈ ہو رہے ہیں۔")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
