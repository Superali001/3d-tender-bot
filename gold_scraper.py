import requests
from bs4 import BeautifulSoup
import smtplib
import os
from email.message import EmailMessage

def send_email(report):
    msg = EmailMessage()
    msg['Subject'] = "📈 Daily Gold Rate Update"
    msg['From'] = "superali001@gmail.com"
    msg['To'] = "superali001@gmail.com"
    msg.set_content(report)
    
    password = os.environ.get('EMAIL_PASSWORD')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login("superali001@gmail.com", password)
        smtp.send_message(msg)

def run():
    url = "https://www.goldrateupdate.com/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # ٹیبل کا ڈیٹا تلاش کریں
        table = soup.find('table')
        rows = table.find_all('tr')
        
        report = "📊 Gold Rate Update (Lahore Gold)\n\n"
        
        # ٹیبل کی ہر لائن کو پڑھیں
        for row in rows:
            cols = row.find_all('td')
            if len(cols) == 2:
                name = cols[0].get_text(strip=True)
                val = cols[1].get_text(strip=True)
                report += f"• {name}: {val}\n"
        
        report += "\nلنک: https://www.goldrateupdate.com/"
        send_email(report)
        print("Data sent successfully!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
