from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from datetime import datetime

def draw_divider(c, y, width):
    c.setLineWidth(0.5)
    c.line(50, y, width - 50, y)

def check_page_break(c, y, height, bottom_margin=50):
    if y < bottom_margin:
        c.showPage()
        y = height - 50
    return y

def clean_tuple_data(raw_tuple):
    try:
        return ", ".join([f"{k}={v}" for part in raw_tuple for k, v in part])
    except Exception:
        return str(raw_tuple)

def generate_pdf_report(domain, ssl_data, headers, ports, techs, file_path):
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    y = height - 50

    # ——— Title & Metadata ———
    y = check_page_break(c, y, height)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(50, y, "CyberGuard Lite Report")
    y -= 30

    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Domain: {domain}")
    y -= 20
    c.drawString(50, y, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y -= 30
    draw_divider(c, y, width)
    y -= 30

    # ——— SSL Section ———
    y = check_page_break(c, y, height)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "SSL Certificate")
    y -= 20
    c.setFont("Helvetica", 12)

    if ssl_data.get("valid"):
        y = check_page_break(c, y, height)
        c.drawString(60, y, "Certificate is valid")
        y -= 20
        issuer = clean_tuple_data(ssl_data.get("issuer", "N/A"))
        subject = clean_tuple_data(ssl_data.get("subject", "N/A"))
        y = check_page_break(c, y, height)
        c.drawString(60, y, f"Issuer: {issuer}")
        y -= 20
        y = check_page_break(c, y, height)
        c.drawString(60, y, f"Subject: {subject}")
    else:
        y = check_page_break(c, y, height)
        c.setFillColorRGB(1, 0, 0)
        c.drawString(60, y, f"{ssl_data.get('error', 'Unknown error')}")
        c.setFillColorRGB(0, 0, 0)
    y -= 30
    draw_divider(c, y, width)
    y -= 30

    # ——— HTTP Headers Section ———
    y = check_page_break(c, y, height)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "HTTP Headers")
    y -= 20
    c.setFont("Helvetica", 12)

    if "error" in headers:
        y = check_page_break(c, y, height)
        c.setFillColorRGB(1, 0, 0)
        c.drawString(60, y, headers["error"])
        c.setFillColorRGB(0, 0, 0)
        y -= 30
    else:
        max_width = width - 120
        for key, val in headers.items():
            line = f"{key}: {val}"
            wrapped = simpleSplit(line, "Helvetica", 12, max_width)
            for i, sub in enumerate(wrapped):
                y = check_page_break(c, y, height)
                indent = 60 if i == 0 else 80
                c.drawString(indent, y, sub)
                y -= 15
            y -= 5
        y -= 10
    draw_divider(c, y, width)
    y -= 30

    # ——— Open Ports Section ———
    y = check_page_break(c, y, height)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Open Ports")
    y -= 20
    c.setFont("Helvetica", 12)

    if isinstance(ports, list):
        if ports:
            port_str = ", ".join(map(str, ports))
            wrapped = simpleSplit(port_str, "Helvetica", 12, width - 120)
            for sub in wrapped:
                y = check_page_break(c, y, height)
                c.drawString(60, y, sub)
                y -= 15
        else:
            y = check_page_break(c, y, height)
            c.drawString(60, y, "No open ports detected.")
            y -= 15
    else:
        y = check_page_break(c, y, height)
        c.setFillColorRGB(1, 0, 0)
        c.drawString(60, y, ports.get("error", "Scan failed"))
        c.setFillColorRGB(0, 0, 0)
        y -= 15
    y -= 15
    draw_divider(c, y, width)
    y -= 30

    # ——— Tech Stack Section ———
    y = check_page_break(c, y, height)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Detected Tech Stack")
    y -= 20
    c.setFont("Helvetica", 12)

    tech_line = ", ".join(techs) if techs else "Unknown"
    wrapped = simpleSplit(tech_line, "Helvetica", 12, width - 120)
    for sub in wrapped:
        y = check_page_break(c, y, height)
        c.drawString(60, y, sub)
        y -= 15
    y -= 20
    draw_divider(c, y, width)
    y -= 30

    # ——— Footer ———
    y = check_page_break(c, y, height)
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 30, "Report generated by CyberGuard Lite")
    c.drawRightString(width - 50, 30, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    c.save()
