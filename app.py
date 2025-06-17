import re
import streamlit as st
import os
from scanner import check_ssl, get_http_headers, check_tech_stack
from report_generator import generate_pdf_report

def clean_domain(input_str):
    input_str = input_str.strip().lower()
    input_str = re.sub(r'^https?://', '', input_str)  # remove http or https
    input_str = input_str.split('/')[0]  # remove anything after /
    return input_str

st.set_page_config(page_title="CyberGuard Lite", layout="centered")

st.markdown(
    """
    <div style="text-align: center;">
        <h1 style="font-size: 42px;">🛡️ <span style='color:#00adb5;'>CyberGuard Lite</span></h1>
        <p style="font-size:18px; color: #444;">Scan any website for basic security issues and generate a downloadable PDF report — fast, simple, and free.</p>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("---")

user_input = st.text_input("🔎 Enter website URL", placeholder="e.g. https://nmit.ac.in")
domain = clean_domain(user_input)

if user_input and "." not in user_input:
    st.warning("❗ Please enter a valid domain or URL.")

if st.button("🚀 Run Security Scan") and domain:
    with st.spinner(f"Scanning {domain}..."):
        ssl = check_ssl(domain)
        headers = get_http_headers(domain)
        #ports = scan_ports(domain)
        techs = check_tech_stack(domain)

        report_file = f"{domain}_report.pdf"
        generate_pdf_report(domain, ssl, headers, ports, techs, report_file)

    st.success("✅ Scan Complete!")

    st.markdown("---")
    with st.expander("🔐 SSL Certificate Details"):
        if ssl["valid"]:
            st.success("✅ Certificate is valid.")
            st.json(ssl)
        else:
            st.error(f"❌ {ssl['error']}")


    with st.expander("📦 HTTP Headers"):
        if "error" in headers:
            st.error(f"❌ {headers['error']}")
        else:
            st.json(headers)

    with st.expander("📡 Open Ports"):
        if isinstance(ports, list):
            st.write(", ".join(map(str, ports)) if ports else "No open ports detected")
        else:
            st.error(f"❌ {ports.get('error', 'Scan failed')}")

    with st.expander("🧠 Detected Tech Stack"):
        if techs:
            st.write(", ".join(techs))
        else:
            st.write("Unknown or not detected")

    st.markdown("---")

    report_file = f"{domain}_report.pdf"
    generate_pdf_report(domain, ssl, headers, ports, techs, report_file)

    with open(report_file, "rb") as f:
        st.download_button("📄 Download PDF Report", f, file_name=report_file)

    os.remove(report_file)
st.markdown("---")
st.markdown(
    "<div style='text-align: center; font-size: 13px;'>🔧 Built with ❤️ by Mohit | Powered by Python & Streamlit</div>",
    unsafe_allow_html=True
)
