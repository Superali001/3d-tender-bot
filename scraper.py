import requests
from bs4 import BeautifulSoup
import smtplib
import os
from email.message import EmailMessage

# 1. سرکاری اور پرائیویٹ ویب سائٹس
targets = [
    {"url": "https://epms.ppra.gov.pk/public/tenders/active-tenders", "name": "PPRA_Federal"},
    {"url": "https://ppra.punjab.gov.pk/tenders", "name": "PPRA_Punjab"},
    {"url": "https://epads.punjab.gov.pk/open-opportunities/", "name": "EPADS_Punjab"},
    {"url": "https://www.pitb.gov.pk/tenders", "name": "PITB_Tenders"},
    {"url": "https://kppra.gov.pk/tenders", "name": "KPPRA_KPK"},
    {"url": "https://sppra.org.pk/tenders", "name": "SPPRA_Sindh"},
    {"url": "https://www.nha.gov.pk/tenders/", "name": "NHA_National_Highway"},
    {"url": "https://tenders.pk/tenders/all", "name": "Tenders_PK_Private"}
]

# 2. آپ کے فائنل پروفیشنل کی ورڈز
keywords = [
    "cad cam", "3d design", "3d modeling", "3d model making", 
    "surface modeling", "parametric design", "generative design", 
    "geometric modeling", "solid modeling", "wireframe modeling", 
    "assembly modeling", "mold design", "solidworks", "autocad", 
    "autodesk inventor", "catia", "siemens nx", "ptc creo", "rhino", 
    "blender", "fusion 360", "freecad", "onshape", "openscad", "zbrush", 
    "3ds max", "maya", "parasolid", "acis", "u3d", "pdf 3d", 
    "collada", "gltf", "render",
]

def send_email(keyword, site_name, url):
    msg = EmailMessage()
    msg['Subject'] = f"🚀 HIGH-VALUE ALERT: {keyword.upper()}"
    msg['From'] = "superali001@gmail.com"
    msg['To'] = "superali001@gmail.com"
    
    body = f"""
==================================================
🚀 NEW OPPORTUNITY FOUND | TAJSEED O TAJWEED 🚀
==================================================

🎯 MATCHED SPECIALIZATION: {keyword.upper()}
🌐 SOURCE PLATFORM: {site_name}

🔗 DIRECT ACCESS LINK:
{url}

--------------------------------------------------
💡 PROFESSIONAL NOTE: 
This is a targeted alert for your design & 
manufacturing services. Please review the 
specifications at the link above.
--------------------------------------------------
System Status: Automatic Monitoring Active
==================================================
"""
    msg.set_content(body)
    
    try:
        password = os.environ.get('EMAIL_PASSWORD')
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("superali001@gmail.com", password)
            smtp.send_message(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")

def run_scraper():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    for target in targets:
        try:
            response = requests.get(target["url"], headers=headers, timeout=25)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.get_text().lower()
                
                for k in keywords:
                    if k in text:
                        send_email(k, target['name'], target['url'])
                        break 
        except Exception as e:
            print(f"Error accessing {target['name']}: {e}")

if __name__ == "__main__":
    run_scraper()
