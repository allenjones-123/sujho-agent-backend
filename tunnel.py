import os
from pyngrok import ngrok

# Authenticate ngrok using your free token (This completely bypasses the terminal login bug!)
NGROK_AUTH_TOKEN = "3EBNR4VIzqxOzv5eWi7qvuVzDcN_6YrERNUX41kB16pf8tFMZ"
ngrok.set_auth_token(NGROK_AUTH_TOKEN)

# Start an HTTP tunnel on port 8000
public_url = ngrok.connect(8000)
print("\n" + "="*50)
print(f"🚀 YOUR LIVE PUBLIC URL IS:\n{public_url.public_url}")
print("="*50 + "\n")

# Keep the script alive
import time
while True:
    time.sleep(1)