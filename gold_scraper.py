import requests
from bs4 import BeautifulSoup
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
    url = "https://gold.pk/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # برانڈ کا نام اور ہیڈر
        report = "🌟 Tajseed o Tajweed - Gold & Market Rates\n"
        report += "==========================================\n\n"
        
        # آپ کے بھیجے گئے سورس کوڈ کے مطابق 'goldratehome' کلاس سے ڈیٹا اٹھانا
        rate_elements = soup.find_all('p', class_='goldratehome')
        
        if len(rate_elements) >= 3:
            tola_rate = rate_elements[0].get_text(strip=True)
            ten_gram_rate = rate_elements[1].get_text(strip=True)
            one_gram_rate = rate_elements[2].get_text(strip=True)
            
            # خوبصورت اور صاف ستھرا ٹیبل فارمیٹ
            report += f"{'وزن / کیرٹ (24K)':<20} | {'قیمت (Rs.)':<15}\n"
            report += "-" * 40 + "\n"
            report += f"{'1 Tola (تولہ)':<20} | {tola_rate:<15}\n"
            report += f"{'10 Gram (گرام)':<20} | {ten_gram_rate:<15}\n"
            report += f"{'1 Gram (گرام)':<20} | {one_gram_rate:<15}\n"
        else:
            report += "⚠️ ویب سائٹ کا ڈھانچہ تبدیل ہوا ہے یا ڈیٹا دستیاب نہیں ہے۔\n"
            
        report += "\n------------------------------------------\n"
        report += "تازہ ترین ریٹس: Gold.pk سے حاصل کردہ۔"
        
        send_email(report)
        print("رپورٹ کامیابی سے بھیج دی گئی ہے۔")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
