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
        # پورے پیج کا ٹیکسٹ نکالیں
        text = response.text
        
        report = "🌟 Tajseed o Tajweed - Gold & Market Rates\n"
        report += "========================================\n\n"
        report += f"{'شہر':<15} | {'بڈنگ (Rs.)':<10} | {'آسکنگ (Rs.)':<10}\n"
        report += "-" * 45 + "\n"

        # مخصوص شہروں کے ریٹس کو ٹیکسٹ کے اندر سے تلاش کرنا
        cities = ["Karachi", "Lahore", "Islamabad", "Quetta", "Peshawar"]
        
        for city in cities:
            # یہ کوڈ ہر شہر کے ریٹ کو ٹیکسٹ میں تلاش کر کے الگ کر لے گا
            start_search = f"Gold Rate in {city}"
            if start_search in text:
                # ریٹس نکالنے کے لیے پوزیشننگ
                chunk = text.split(start_search)[1][:100]
                # یہاں سے بڈنگ اور آسکنگ ریٹس نکالیں
                import re
                nums = re.findall(r'\d{6}', chunk)
                if len(nums) >= 2:
                    report += f"{city:<15} | {nums[0]:<10} | {nums[1]:<10}\n"
        
        report += "\nتازہ ترین ریٹس: Gold.pk سے حاصل کردہ۔"
        
        send_email(report)
        print("رپورٹ کامیابی سے بھیج دی گئی ہے۔")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
