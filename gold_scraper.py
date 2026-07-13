import requests
import smtplib
import os
from email.message import EmailMessage

def run():
    # ہم ویب سائٹ کو ایک اصلی موبائل براؤزر کا دھوکہ دیں گے
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    url = "https://gold.pk/"
    
    try:
        # ویب سائٹ کو "کھولنا" (Get Request)
        response = requests.get(url, headers=headers, timeout=30)
        
        # ڈیٹا کو اس کے اصل HTML سے پکڑنا
        if "Rs." in response.text:
            # یہاں ہم صرف وہ حصہ ڈھونڈیں گے جہاں ریٹس لکھے ہوتے ہیں
            start = response.text.find("Gold Rate in Pakistan")
            data = response.text[start:start+2000] # صرف کام کا حصہ
            
            # ای میل بھیجنا
            msg = EmailMessage()
            msg['Subject'] = "📊 Tajseed o Tajweed - Gold Rates"
            msg['From'] = "superali001@gmail.com"
            msg['To'] = "superali001@gmail.com"
            msg.set_content("آج کا ریٹ:\n\n" + data)
            
            password = os.environ.get('EMAIL_PASSWORD')
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login("superali001@gmail.com", password)
                smtp.send_message(msg)
            print("ڈیٹا ریڈ کر کے ای میل کر دیا گیا ہے!")
        else:
            print("ویب سائٹ نے ڈیٹا نہیں دیا، صرف HTML ملا ہے۔")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
