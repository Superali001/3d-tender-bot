import requests
from bs4 import BeautifulSoup
import smtplib
import os
from email.message import EmailMessage

def send_email(report):
    msg = EmailMessage()
    msg['Subject'] = "📊 Tajseed o Tajweed - مکمل مارکیٹ رپورٹ"
    msg['From'] = "superali001@gmail.com"
    msg['To'] = "superali001@gmail.com"
    msg.set_content(report)
    password = os.environ.get('EMAIL_PASSWORD')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login("superali001@gmail.com", password)
        smtp.send_message(msg)

def run():
    url = "https://gold.pk/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        report = "🌟 Tajseed o Tajweed - مکمل مارکیٹ اور کوالٹی رپورٹ\n"
        report += "=================================================================================\n\n"
        
        # 1. Gold Rate Chart (Weightage & Karat Table)
        report += "--- 1. گولڈ ریٹس (مختلف وزن اور کیرٹ) ---\n"
        gold_table = soup.find('table')
        if gold_table:
            for row in gold_table.find_all('tr'):
                cols = [col.get_text(strip=True) for col in row.find_all(['th', 'td'])]
                if cols:
                    # Formats each cell to a clean 20-character wide column
                    report += "".join(f"{col:<20}" for col in cols) + "\n"
        report += "\n" + "="*81 + "\n\n"
        
        # 2. Live Market, City Rates & Silver Table
        report += "--- 2. لائیو مارکیٹ اور شہروں کے ریٹس ---\n"
        tables = soup.find_all('div', class_='progress-table')
        if len(tables) > 0:
            # Fetching only top-level column divs to prevent data overlapping
            rows = tables[0].find_all('div', class_='table-row')
            for row in rows:
                cols = [col.get_text(strip=True) for col in row.find_all('div', recursive=False)]
                if cols:
                    report += "".join(f"{col:<20}" for col in cols) + "\n"
        report += "\n" + "="*81 + "\n\n"
        
        # 3. 15-Days Historical Trend Chart
        report += "--- 3. گزشتہ 15 دنوں کا ٹرینڈ (مکمل چارٹ) ---\n"
        history_wrap = soup.find('div', class_='progress-table-wrap')
        
        # Fallback to secondary table array position if layout shifts
        target_history = history_wrap if history_wrap else (tables[1] if len(tables) > 1 else None)
        
        if target_history:
            history_rows = target_history.find_all('div', class_='table-row')
            for row in history_rows:
                cols = [col.get_text(strip=True) for col in row.find_all('div', recursive=False)]
                if cols:
                    report += "".join(f"{col:<20}" for col in cols) + "\n"
        report += "\n" + "="*81 + "\n\n"

        # 4. Silver and Gold Purity Details
        report += "--- 4. سلور اور گولڈ پوریٹی (معیار کی تفصیلات) ---\n"
        purity_div = soup.find('div', class_='text14')
        if purity_div:
            report += purity_div.get_text(separator='\n', strip=True) + "\n"

        report += "\n=================================================================================\n"
        report += "تازہ ترین اپڈیٹ: Gold.pk | Tajseed o Tajweed"
        
        send_email(report)
        print("Success: Fixed-width table formatted report has been delivered successfully.")
            
    except Exception as e:
        print(f"Error executing scraper layout: {e}")

if __name__ == "__main__":
    run()
