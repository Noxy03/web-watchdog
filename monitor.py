import requests
import hashlib
import time
import os
import difflib
from bs4 import BeautifulSoup

# --- CONFIGURATION ---
# Replace with your Discord Webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/..." 
URL_FILE = "urls.txt"
CHECK_INTERVAL = 3600  # Default: 1 hour in seconds 

last_texts = {}

def notify_discord(url, diff_text):
    """Sends a formatted notification to Discord"""
    if len(diff_text) > 1500:
        diff_text = diff_text[:1500] + "\n... (truncated)"
        
    message = {
        "content": f"🔔 **Update detected on:** {url}",
        "embeds": [{
            "title": "Changes (Text Comparison)",
            "description": f"```diff\n{diff_text}\n```",
            "color": 3066993 
        }]
    }
    try:
        requests.post(WEBHOOK_URL, json=message)
    except Exception as e:
        print(f"Discord Error: {e}")

def get_clean_text(url):
    """Extracts visible text from the website, ignoring headers/footers"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        # Remove noisy elements
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()

        lines = [line.strip() for line in soup.get_text().splitlines() if line.strip()]
        return lines
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def monitor():
    print("--- WebWatchdog V3 (Diff-Mode) started ---")
    
    # Initial scan
    if not os.path.exists(URL_FILE):
        print(f"Error: {URL_FILE} not found!")
        return

    for url in [u.strip() for u in open(URL_FILE) if u.strip()]:
        last_texts[url] = get_clean_text(url)
        print(f"Initialized: {url}")

    while True:
        time.sleep(CHECK_INTERVAL)
        urls = [u.strip() for u in open(URL_FILE) if u.strip()]
        
        for url in urls:
            current_text_lines = get_clean_text(url)
            
            if url not in last_texts:
                last_texts[url] = current_text_lines
                continue

            if current_text_lines and current_text_lines != last_texts[url]:
                # Generate Diff
                diff = difflib.ndiff(last_texts[url], current_text_lines)
                changes = [line for line in diff if line.startswith('+ ') or line.startswith('- ')]
                
                if changes:
                    diff_output = "\n".join(changes)
                    notify_discord(url, diff_output)
                    print(f"Update sent to Discord: {url}")
                
                last_texts[url] = current_text_lines
            else:
                print(f"Check ok: {url}")

if __name__ == "__main__":
    monitor()