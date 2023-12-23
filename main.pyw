import base64
import random
import requests
import tkinter as tk
from tkinter import ttk, scrolledtext, simpledialog

WEBHOOK_URL = None

def generate_random_token():
    try:
        b64_user_id = base64.b64encode(str(random.randint(100000000000000000, 999999999999999999)).encode()).decode()
        token = f"{b64_user_id}.{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5))}.{''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=27))}"
        return token
    except Exception as e:
        return f"Error generating token: {str(e)}"

def check_token_validity(token):
    try:
        headers = {"Content-Type": "application/json", "authorization": token}
        response = requests.get("https://discordapp.com/api/v6/users/@me/library", headers=headers)
        return response.status_code == 200
    except Exception as e:
        return False

def generate_tokens():
    num_tokens = simpledialog.askinteger("Token Generator", "How many tokens do you want to generate?")
    if num_tokens is not None:
        result_text = ""
        for _ in range(num_tokens):
            token = generate_random_token()
            result_text += f"Token: {token}\n{'-' * 50}\n"
            with open("tokens.txt", "a") as f:
                f.write(f"{token}\n")
                if WEBHOOK_URL:
                    send_webhook(token)
        text_widget.delete(1.0, tk.END)  # Clear previous text
        text_widget.insert(tk.END, result_text)
        text_widget.see(tk.END)

def check_tokens():
    tokens = text_widget.get(1.0, tk.END).splitlines()
    result_text = ""
    for token in tokens:
        if token.strip():
            is_valid = check_token_validity(token)
            result_text += f"Token {token} is {'valid' if is_valid else 'invalid'}.\n\n"
            if is_valid:
                with open("valid_tokens.txt", "a") as f:
                    f.write(f"{token}\n")
    text_widget.delete(1.0, tk.END)  # Clear previous text
    text_widget.insert(tk.END, result_text)
    text_widget.see(tk.END)

def exit_app():
    root.destroy()

def send_webhook(token):
    try:
        headers = {"Content-Type": "application/json"}
        payload = {
            "content": f"New valid token: {token}"
        }
        response = requests.post(WEBHOOK_URL, json=payload, headers=headers)
        response.raise_for_status()
        print("Token sent to webhook successfully.")
    except Exception as e:
        print(f"Error sending token to webhook: {str(e)}")

def set_webhook():
    global WEBHOOK_URL
    webhook_url = simpledialog.askstring("Webhook URL", "Enter your webhook URL:")
    if webhook_url and validate_webhook(webhook_url):
        WEBHOOK_URL = webhook_url
        with open("webhook.txt", "w") as f:
            f.write(WEBHOOK_URL)
        print(f"Webhook URL set to: {WEBHOOK_URL}")
    else:
        print("Invalid webhook URL. Please try again.")

def validate_webhook(webhook_url):
    try:
        headers = {"Content-Type": "application/json"}
        response = requests.head(webhook_url, headers=headers)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Error validating webhook URL: {str(e)}")
        return False

def load_webhook():
    global WEBHOOK_URL
    try:
        with open("webhook.txt", "r") as f:
            WEBHOOK_URL = f.read().strip()
            if WEBHOOK_URL and not validate_webhook(WEBHOOK_URL):
                print("Invalid webhook URL. Please set a new webhook.")
    except FileNotFoundError:
        print("Webhook file not found. Please set a new webhook.")

# Load the webhook URL on startup
load_webhook()

# Create the main window
root = tk.Tk()
root.title("F4llTokens")

# Create and pack widgets with improved styling
style = ttk.Style()

# Configure Frame
style.configure("TFrame", background="#2c2f33")

# Configure Label
style.configure("TLabel", padding=10, font=('Helvetica', 14), background="#2c2f33", foreground="#ffffff")

# Configure Button
style.configure("TButton", padding=10, font=('Helvetica', 12), borderwidth=0, borderradius=5)

# Configure button colors
style.map("TButton",
          background=[('active', '#677bc4'), ('pressed', '#677bc4')],
          foreground=[('pressed', '#ffffff'), ('active', '#ffffff')])

frame = ttk.Frame(root, style="TFrame")
frame.pack(pady=20)

label = ttk.Label(frame, text="Welcome to F4llTokens", style="TLabel")
label.grid(row=0, column=0, columnspan=3, pady=10)

generate_button = ttk.Button(frame, text="Generate Tokens", command=generate_tokens, style="TButton")
generate_button.grid(row=1, column=0, pady=5, padx=10)

webhook_button = ttk.Button(frame, text="Set Webhook", command=set_webhook, style="TButton")
webhook_button.grid(row=1, column=1, pady=5, padx=10)

check_button = ttk.Button(frame, text="Check Tokens", command=check_tokens, style="TButton")
check_button.grid(row=1, column=2, pady=5, padx=10)

text_widget = scrolledtext.ScrolledText(frame, width=70, height=15, wrap=tk.WORD)
text_widget.grid(row=2, column=0, columnspan=3, pady=10, padx=10)

exit_button = ttk.Button(frame, text="Exit", command=exit_app, style="TButton")
exit_button.grid(row=3, column=0, columnspan=3, pady=10)

# Start the GUI event loop
root.mainloop()
