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
    "cad cam", "3d design", "3d modeling", "3d model making", "3d printing", 
    "3d scanner", "cnc machining", "industrial design", 
    "prototyping", "metal casting", "jewelry design",
    "product development", "die making", "precision engineering"
    "cad", "cam", "cae", "cnc", "3d design", "3d modeling", 
    "3d model making", "3d printing", "3d scanner", "cnc machining", 
    "industrial design", "prototyping", "metal casting", "jewelry design", 
    "product development", "die making", "precision engineering", "reverse engineering", 
    "rapid prototyping", "laser cutting", "wire edm", "die casting", "mold making", 
    "surface modeling", "parametric design", "generative design", "mechanical engineering", 
    "aerospace engineering", "quality assurance", "asme standards", 
    "iso standards", "g-code", "metrology", "solidworks", "autocad", 
    "autodesk inventor", "catia", "siemens nx", "ptc creo", "rhino", 
    "blender", "fusion 360", "mastercam", "ansys", "defense", "aerospace", 
    "automotive", "consumer electronics", "medical devices", "robotics", 
    "marine engineering", "heavy machinery", "railway design", "hvac", 
    "structural engineering", "piping design", "plant layout", "mold design", 
    "stamping die", "jig and fixture", "sheet metal fabrication", "weldment design", 
    "foundry tooling", "investment casting", "vacuum forming", "plastic extrusion", 
    "progressive die", "pdm", "mes", "erp", "mfg", "mbd", "pmi", "dfx", "camworks", 
    "hypermill", "esprit", "featurecam", "powermill", "zbrush", "3ds max", "maya", 
    "freecad", "onshape", "openscad", "tribology", "kinematics", "mechatronics", 
    "ergonomics", "finite element method", "computational fluid dynamics", "cfd", 
    "thermal analysis", "linear analysis", "non-linear analysis", "structural analysis", 
    "gdt", "surface roughness", "tolerance stackup", "geometric modeling", "solid modeling", 
    "wireframe modeling", "assembly modeling", "weldment", "piping", "tubing", "cabling", 
    "harness design", "capping", "overmolding", "blow molding", "thermoforming", "sand casting", 
    "die stamping", "laser welding", "plasma cutting", "waterjet cutting", "edm machining", 
    "4 axis cnc", "5 axis cnc", "swiss lathe", "turn mill", "mill turn", "additive mfg", "sls", 
    "sla", "fdm", "dlms", "slm", "binder jetting", "material jetting", "direct energy deposition", 
    "3d inspection", "cmm", "optical scanning", "structured light", "laser scanning", 
    "photogrammetry", "ndt", "non destructive testing", "x ray inspection", "ct scanning", 
    "dimensional inspection", "first article inspection", "fai", "ppap", "apqp", "six sigma", 
    "lean manufacturing", "industry 4 0", "iiot", "smart manufacturing", "cyberphysical systems", 
    "digital thread", "cde", "common data environment", "ifc", "industry foundation classes", 
    "cobie", "navisworks", "revit", "microstation", "bentley", "arcgis", "qgis", "point cloud", 
    "lidar", "dem", "digital elevation model", "photogrammetry data", "spatial data", "geospatial", 
    "hydrographic", "topographic", "military engineering", "naval architecture", "subsea engineering", 
    "offshore engineering", "pressure vessel", "asme sec viii", "piping codes", "asme b31 3", 
    "api standards", "din standards", "bsi standards", "jis standards", "mil std", "mil prf", 
    "def stan", "stanag", "fed spec", "nist 800 171", "cmmc", "cybersecurity compliance", 
    "ear compliance", "export control", "proprietary data", "trade secret", "ip protection", 
    "ndd", "neutral data format", "parasolid", "acis", "sat", "sab", "vdafs", "vda", "prc", 
    "u3d", "pdf 3d", "collada", "dae", "gltf", "glb", "ply", "xyz", "las", "laz"
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
