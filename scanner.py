import requests
import socket
import ssl
#import nmap
from bs4 import BeautifulSoup

def check_ssl(domain):
    context = ssl.create_default_context()
    try:
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                return {"valid": True, "issuer": cert.get("issuer"), "subject": cert.get("subject")}
    except Exception as e:
        return {"valid": False, "error": str(e)}

def get_http_headers(domain):
    try:
        response = requests.get(f"https://{domain}", timeout=5)
        return dict(response.headers)
    except Exception as e:
        return {"error": str(e)}

# def scan_ports(domain):
#     scanner = nmap.PortScanner()
#     try:
#         scanner.scan(domain, '20-1024')  # Basic range of ports
#         open_ports = []
#         for proto in scanner[domain].all_protocols():
#             ports = scanner[domain][proto].keys()
#             open_ports.extend(ports)
#         return sorted(open_ports)
#     except Exception as e:
#         return {"error": str(e)}

def check_tech_stack(domain):
    techs = set()
    try:
        res = requests.get(f"https://{domain}", timeout=5)
        html = res.text
        headers = res.headers
        soup = BeautifulSoup(html, 'html.parser')

        # 🧠 Check meta generator
        generator = soup.find("meta", {"name": "generator"})
        if generator and generator.get("content"):
            techs.add(generator["content"])

        # 🧱 Check server headers
        if "server" in headers:
            techs.add(f"Server: {headers['server']}")

        if "x-powered-by" in headers:
            techs.add(f"X-Powered-By: {headers['x-powered-by']}")

        # 🎯 Pattern matching in HTML
        if "wp-content" in html:
            techs.add("WordPress")

        if "cdn.shopify.com" in html:
            techs.add("Shopify")

        if "drupal.js" in html:
            techs.add("Drupal")

        if "static.wixstatic.com" in html:
            techs.add("Wix")

        if "squarespace.com" in html:
            techs.add("Squarespace")

        if "react" in html.lower():
            techs.add("React (likely)")

        if "vue" in html.lower():
            techs.add("Vue.js (likely)")

        return list(techs) if techs else ["Unknown"]
    except Exception as e:
        return [f"Error: {str(e)}"]