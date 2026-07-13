import requests
from bs4 import BeautifulSoup
import smtplib
import os
from email.message import EmailMessage

def send_email(report):
    msg = EmailMessage()
    msg['Subject'] = "📊 Tajseed o Tajweed - لائیو مارکیٹ رپورٹ"
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
        
        report = "🌟 Tajseed o Tajweed - لائیو مارکیٹ رپورٹ\n"
        report += "==================================================\n\n"
        
        # شہروں کے ریٹس تلاش کرنا
        report += f"{'شہر':<15} | {'بڈنگ':<10} | {'آسکنگ':<10}\n"
        report += "-" * 40 + "\n"
        
        # ویب سائٹ کے ہر رو کو تلاش کریں جس میں شہر کا ڈیٹا ہے
        # Gold.pk میں ہر شہر ایک 'table-row' کلاس کے اندر ہے
        rows = soup.find_all('div', class_='table-row')
        
        for row in rows:
            # کالمز نکالیں
            cols = row.find_all('div', class_=lambda x: x and 'column' in x)
            if len(cols) >= 3:
                city = cols[0].get_text(strip=True)
                bid = cols[2].get_text(strip=True)
                ask = cols[3].get_text(strip=True)
                if city and bid and ask:
                    report += f"{city:<15} | {bid:<10} | {ask:<10}\n"
        
        report += "\nتازہ ترین اپڈیٹ: " + soup.find('div', class_='text14').get_text(strip=True)[:50]
        
        send_email(report)
        print("کامیاب! ٹیبل والا ڈیٹا ای میل کر دیا گیا ہے۔")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
