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
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # برانڈ کا نام
        report = "🌟 Tajseed o Tajweed - Gold & Market Rates\n"
        report += "==========================================\n\n"
        
        # ٹیبل ہیڈر
        report += f"{'شہر':<12} | {'بڈنگ (Rs.)':<12} | {'آسکنگ (Rs.)':<12}\n"
        report += "-" * 40 + "\n"

        # ویب سائٹ پر موجود تمام ٹیبل روز (rows) کو تلاش کرنا
        for row in soup.find_all('tr'):
            cols = row.find_all('td')
            # اگر رو میں 4 کالم ہیں (شہر، سمبل، بڈنگ، آسکنگ)
            if len(cols) >= 4:
                city = cols[0].get_text(strip=True).replace("Gold Rate in ", "")
                bidding = cols[2].get_text(strip=True)
                asking = cols[3].get_text(strip=True)
                
                # صرف ان رو کو لیں جن میں ریٹس ہیں (عدد موجود ہوں)
                if bidding.isdigit() and asking.isdigit():
                    report += f"{city:<12} | {bidding:<12} | {asking:<12}\n"

        report += "\nتازہ ترین ریٹس: Gold.pk سے حاصل کردہ۔"
        
        send_email(report)
        print("ٹیبل فارمیٹ میں رپورٹ بھیج دی گئی ہے۔")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
