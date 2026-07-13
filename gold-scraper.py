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
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        # یہاں آپ ویب سائٹ کا ڈیٹا نکال رہے ہیں
        title = soup.title.string if soup.title else "Gold Update"
        report = f"Gold Rate Update: {title} \n\nDirect Link: {url} \n\nSystem successfully fetched latest rates."
        send_email(report)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
