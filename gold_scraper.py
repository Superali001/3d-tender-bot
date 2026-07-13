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
        
        # برانڈ نیم اور ہیڈر
        report = "🌟 Tajseed o Tajweed - Gold & Market Rates\n"
        report += "========================================\n\n"
        
        # شہروں کے ریٹس کا ٹیبل نکالنا
        report += f"{'شہر':<15} | {'بڈنگ (Rs.)':<12} | {'آسکنگ (Rs.)':<12}\n"
        report += "-" * 45 + "\n"
        
        # ویب سائٹ کے ٹیبل سے ڈیٹا تلاش کرنا
        rows = soup.find_all('tr')
        cities = ['Karachi', 'Lahore', 'Islamabad', 'Quetta', 'Peshawar']
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 3:
                city_name = cols[0].get_text(strip=True)
                # صرف ہمارے مطلوبہ شہروں کو فلٹر کرنا
                if any(city in city_name for city in cities):
                    bidding = cols[2].get_text(strip=True)
                    asking = cols[3].get_text(strip=True)
                    report += f"{city_name.replace('Gold Rate in ', ''):<15} | {bidding:<12} | {asking:<12}\n"
        
        report += "\nتازہ ترین ریٹس: Gold.pk سے حاصل کردہ۔"
        
        send_email(report)
        print("ٹیبل فارمیٹ میں رپورٹ کامیابی سے بھیج دی گئی ہے۔")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
