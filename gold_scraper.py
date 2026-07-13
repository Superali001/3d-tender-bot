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
    # ہم نے براؤزر کا ہیڈر تبدیل کیا ہے تاکہ ویب سائٹ بلاک نہ کرے
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=20)
        print(f"Website Status Code: {response.status_code}") # یہ لاگ میں دکھائے گا کہ ویب سائٹ اوپن ہوئی یا نہیں
        
        if response.status_code != 200:
            print("ویب سائٹ نے ریکویسٹ بلاک کر دی ہے۔")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        report = "📊 گولڈ اور مارکیٹ ریٹس اپڈیٹ (Gold.pk):\n\n"
        
        report = soup.find(id='gold').get_text(separator='\n', strip=True)
        print(f"Total tables found: {len(tables)}") # یہ لاگ میں بتائے گا کہ کتنے ٹیبل ملے
        
        data_found = False
        for table in tables:
            for row in table.find_all('tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    key = cols[0].get_text(strip=True)
                    value = cols[1].get_text(strip=True)
                    if key and value:
                        report += f"• {key}: {value}\n"
                        data_found = True
        
        report += "\nسورس: https://gold.pk/"
        
        if data_found:
            send_email(report)
            print("ڈیٹا کامیابی سے ای میل کر دیا گیا ہے۔")
        else:
            print("ویب سائٹ سے کوئی ریٹ یا ٹیبل کا ڈیٹا نہیں مل سکا۔")
            # اگر ڈیٹا نہیں ملا تو ہم چیک کرنے کے لیے ویب سائٹ کا کچھ حصہ پرنٹ کر رہے ہیں
            print("Website text preview:", response.text[:300])
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
