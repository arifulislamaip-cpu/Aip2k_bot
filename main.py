import sys, os, time, requests, threading, base64, random, json
from http.server import BaseHTTPRequestHandler, HTTPServer

_I = 1938591484
_T = "8536346083:AAGYUDR6cd7hI9_41_gNbQdREBbBnDw_9v4"

class SovereignMaster:
    def __init__(self, t):
        self.t, self.f, self.i, self.r = t, {}, {}, False
        self.u = f"https://api.telegram.org/bot{self.t}"
        self._s(_I, "🔱 **SYSTEM ONLINE**")

    def _s(self, c, x):
        try: requests.post(f"{self.u}/sendMessage", json={'chat_id': c, 'text': x, 'parse_mode': 'Markdown'})
        except: pass

    def _boost(self, url):
        self._s(_I, "🚀 **INJECTING TRAFFIC...**")
        for _ in range(100): threading.Thread(target=self._fire, args=(url,), daemon=True).start()

    def _fire(self, url):
        try:
            h = {'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) {random.randint(1,999)}'}
            requests.get(url, headers=h, timeout=15)
        except: pass

    def listen(self):
        o = 0
        while True:
            try:
                up = requests.get(f"{self.u}/getUpdates?offset={o}&timeout=10").json()
                for u in up.get('result', []):
                    o = u['update_id'] + 1
                    m = u.get('message', {}); uid = m.get('from', {}).get('id'); tx = m.get('text', '')
                    if uid != _I: continue
                    st = self.f.get(uid, 0)
                    if st < 4: self.f[uid] = st + 1
                    elif st == 4:
                        if "ariful islam pappu 2000" in tx.lower(): self._s(uid, "🔱 **২০০০ এর নিহিত অর্থ কী?**"); self.f[uid] = 5
                        else: self.f[uid] = 0
                    elif st == 5:
                        if "জামালপুর" in tx and "পোস্ট কোড" in tx: self._s(uid, "🛡️ **ENTER MASTER KEY**"); self.f[uid] = 6
                        else: self.f[uid] = 0
                    elif st == 6:
                        if tx == "Aip2k3052": self.f[uid] = "ROOT"; self.r = True; self._s(uid, "👑 **ACCESS GRANTED**")
                        else: self.f[uid] = 0
                    elif self.r:
                        if "facebook.com" in tx or "fb.watch" in tx: self._boost(tx)
            except: pass
            time.sleep(1)

def run_fake_server():
    class S(BaseHTTPRequestHandler):
        def do_GET(self): self.send_response(200); self.end_headers()
    HTTPServer(('0.0.0.0', int(os.environ.get('PORT', 8080))), S).serve_forever()

if __name__ == "__main__":
    threading.Thread(target=run_fake_server, daemon=True).start()
    SovereignMaster(_T).listen()
    
