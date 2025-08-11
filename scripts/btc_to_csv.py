#!/usr/bin/env python3
# API'den (CoinGecko) BTC fiyatını çekip CSV'ye ekler.
import os, csv, time, requests

URL = "https://api.coingecko.com/api/v3/simple/price"
PARAMS = {"ids": "bitcoin", "vs_currencies": "usd,eur"}
CSV_PATH = os.getenv("CSV_PATH", "btc_price.csv")

def ensure_header(path: str):
    """Dosya yoksa ya da boşsa başlık satırını yazar."""
    need_header = True
    if os.path.exists(path) and os.path.getsize(path) > 0:
        need_header = False
    if need_header:
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["timestamp", "usd", "eur"])
            w.writeheader()

def fetch_price(max_retries=3, timeout=10):
    for i in range(max_retries):
        try:
            r = requests.get(URL, params=PARAMS, timeout=timeout)
            # Geçici hatalarda yeniden dene
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(2 ** i)
                continue
            r.raise_for_status()
            data = r.json()["bitcoin"]
            return float(data["usd"]), float(data["eur"])
        except requests.RequestException:
            if i == max_retries - 1:
                raise
            time.sleep(2 ** i)

def append_row(path: str, row: dict):
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["timestamp", "usd", "eur"])
        w.writerow(row)

def main():
    ensure_header(CSV_PATH)
    usd, eur = fetch_price()
    row = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "usd": usd,
        "eur": eur,
    }
    append_row(CSV_PATH, row)
    print(f"[OK] Yazıldı → {CSV_PATH}: {row}")

if __name__ == "__main__":
    main()
