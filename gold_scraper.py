import requests
import re
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
        content = response.text
        
        report = "🌟 Tajseed o Tajweed - Gold & Market Rates\n"
        report += "==========================================\n\n"
        report += f"{'شہر':<12} | {'بڈنگ (Rs.)':<12} | {'آسکنگ (Rs.)':<12}\n"
        report += "-" * 40 + "\n"

        # Regex پیٹرن جو ویب سائٹ کے سورس کوڈ سے ریٹس نکالے گا
        # یہ پیٹرن: "Gold Rate in CityName" کے بعد آنے والے نمبرز پکڑتا ہے
        pattern = r"Gold Rate in (.*?)\s*</td>.*?<td>.*?</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>"
        matches = re.findall(pattern, content, re.DOTALL)

        for match in matches:
            city = match[0].strip()
            bidding = match[1].strip()
            asking = match[2].strip()
            # صرف اہم شہروں کو فلٹر کرنا
            if city in ["Karachi", "Lahore", "Islamabad", "Quetta", "Peshawar"]:
                report += f"{city:<12} | {bidding:<12} | {asking:<12}\n"

        report += "\nتازہ ترین ریٹس: Gold.pk سے حاصل کردہ۔"
        
        send_email(report)
        print("رپورٹ کامیابی سے بھیج دی گئی ہے۔")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
