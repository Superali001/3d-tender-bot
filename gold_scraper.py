import requests
from bs4 import BeautifulSoup
import smtplib
import os
from email.message import EmailMessage

def run():
    # اس بار ہم ہیڈر کو مکمل براؤزر جیسا بنا رہے ہیں
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    url = "https://gold.pk/"
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # ویب سائٹ کے مرکزی ڈیٹا والے حصے (Container) کو ڈھونڈنا
        content = soup.get_text(separator='\n', strip=True)
        
        # اگر ٹیکسٹ بہت چھوٹا ہے تو اس کا مطلب ڈیٹا نہیں ملا
        if len(content) < 500:
            print("ڈیٹا نہیں ملا - ویب سائٹ نے بلاک کر دیا ہے۔")
            return

        # ای میل بھیجنا
        msg = EmailMessage()
        msg['Subject'] = "📈 مکمل گولڈ ریٹس رپورٹ"
        msg['From'] = "superali001@gmail.com"
        msg['To'] = "superali001@gmail.com"
        msg.set_content(content[:4000]) # صرف 4000 الفاظ تک ای میل بھیجیں گے
        
        password = os.environ.get('EMAIL_PASSWORD')
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("superali001@gmail.com", password)
            smtp.send_message(msg)
        print("کامیاب!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
