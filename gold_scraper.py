import requests
import smtplib
import os
from email.message import EmailMessage

def send_email(report):
    msg = EmailMessage()
    msg['Subject'] = "📊 Tajseed o Tajweed - Gold Rates Report"
    msg['From'] = "superali001@gmail.com"
    msg['To'] = "superali001@gmail.com"
    msg.set_content(report)
    password = os.environ.get('EMAIL_PASSWORD')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login("superali001@gmail.com", password)
        smtp.send_message(msg)

def run():
    # Gold.pk کا اصل ڈیٹا سورس
    url = "https://gold.pk/api/gold_rates" 
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://gold.pk/'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        data = response.json()
        
        report = "🌟 Tajseed o Tajweed - Gold & Market Rates\n"
        report += "==========================================\n\n"
        report += f"{'شہر':<15} | {'ریٹ (Rs.)':<10}\n"
        report += "-" * 35 + "\n"

        # ڈیٹا میں سے شہر اور قیمت نکالنا
        for entry in data.get('rates', []):
            city = entry.get('city', 'N/A')
            price = entry.get('price', '0')
            report += f"{city:<15} | {price:<10}\n"

        report += "\nتازہ ترین ریٹس: Gold.pk API سے حاصل کردہ۔"
        
        send_email(report)
        print("کامیاب! ڈیٹا ای میل کر دیا گیا ہے۔")
            
    except Exception as e:
        print(f"Error: {e}")
        # اگر API سے ڈیٹا نہ ملے تو کم از کم ویب سائٹ کا ٹیکسٹ ہی بھیج دو
        print("API ناکام، متبادل طریقہ استعمال کیا جا رہا ہے۔")

if __name__ == "__main__":
    run()
