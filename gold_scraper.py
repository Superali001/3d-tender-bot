import requests
from bs4 import BeautifulSoup
import smtplib
import os
import time
from email.message import EmailMessage

def send_email(subject, report):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = "superali001@gmail.com"
    msg['To'] = "superali001@gmail.com"
    msg.set_content(report)
    password = os.environ.get('EMAIL_PASSWORD')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login("superali001@gmail.com", password)
        smtp.send_message(msg)

def run():
    url = "https://gold.pk/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
    
    # 1. نیٹ ورک ٹیسٹ (اگر سائٹ ڈاؤن ہو تو 3 بار کوشش کرے)
    for attempt in range(3):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200: break
        except:
            time.sleep(5)
    else:
        send_email("⚠️ ALERT: Gold.pk سے رابطہ نہیں ہو رہا", "سسٹم نے ویب سائٹ تک رسائی کی کوشش کی لیکن ناکام رہا۔")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    report = "🌟 Tajseed o Tajweed - مکمل گولڈ مارکیٹ رپورٹ\n"
    report += "==================================================\n\n"

    # 2. لائیو گولڈ اور سلور ریٹس
    report += "--- لائیو مارکیٹ ریٹس ---\n"
    report += f"{'Metal':<12} | {'Bid':<10} | {'Ask':<10}\n"
    report += "-" * 35 + "\n"
    rows = soup.find_all('div', class_='table-row')
    for row in rows:
        cols = row.find_all('div')
        if len(cols) >= 4 and ("Gold" in cols[0].get_text() or "Silver" in cols[0].get_text()):
            report += f"{cols[0].get_text():<12} | {cols[2].get_text():<10} | {cols[3].get_text():<10}\n"

    # 3. گزشتہ 15 دن کا ٹرینڈ
    report += "\n--- گزشتہ 15 دنوں کا ٹرینڈ (24K) ---\n"
    report += f"{'تاریخ':<12} | {'کلوزنگ ریٹ':<10}\n"
    report += "-" * 25 + "\n"
    for row in rows:
        cols = row.find_all('div')
        # صرف وہی روز شامل ہوں جن میں تاریخ لکھی ہو
        if len(cols) > 2 and any(month in cols[0].get_text() for month in ["Jul", "Jun"]):
            report += f"{cols[0].get_text():<12} | {cols[1].get_text():<10}\n"

    # 4. پوریٹی (معیار) کی تفصیلات
    report += "\n--- گولڈ اور سلور پوریٹی چارٹ ---\n"
    purity_div = soup.find('div', class_='text14')
    if purity_div:
        full_text = purity_div.get_text(separator='\n', strip=True)
        # 24K سے نیچے والا حصہ پوریٹی کے لیے نکالیں
        if "24 Karat" in full_text:
            report += full_text[full_text.find("24 Karat"):]

    report += "\n\nتازہ ترین اپڈیٹ: " + time.strftime("%d %b %Y, %H:%M") + " PST\n"
    report += "Tajseed o Tajweed - آپ کا بااعتماد جیولری پارٹنر"

    # رپورٹ ای میل کریں
    send_email("📊 Tajseed o Tajweed - ڈیلی مارکیٹ رپورٹ", report)
    print("کامیاب: رپورٹ بھیج دی گئی ہے۔")

if __name__ == "__main__":
    run()
