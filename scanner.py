import ssl
import socket
import requests
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

def check_tech_stack(domain):
    techs = set()
    try:
        res = requests.get(f"https://{domain}", timeout=5)
        html = res.text.lower()
        headers = res.headers
        soup = BeautifulSoup(html, 'html.parser')

        gen = soup.find("meta", {"name": "generator"})
        if gen and gen.get("content"):
            techs.add(gen["content"])

        if "server" in headers:
            techs.add(f"Server: {headers['server']}")
        if "x-powered-by" in headers:
            techs.add(f"X-Powered-By: {headers['x-powered-by']}")

        # simple HTML patterns
        for marker, name in [
            ("wp-content", "WordPress"),
            ("cdn.shopify.com", "Shopify"),
            ("drupal.js", "Drupal"),
            ("static.wixstatic.com", "Wix"),
            ("squarespace.com", "Squarespace"),
        ]:
            if marker in html:
                techs.add(name)

        if "react" in html:
            techs.add("React (likely)")
        if "vue" in html:
            techs.add("Vue.js (likely)")

        return list(techs) if techs else ["Unknown"]
    except Exception as e:
        return [f"Error: {e}"]
