import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

URL = "https://asloterias.com.br/resultados-da-mega-sena"

def fetch_megasena():
    print("Fetching Mega-Sena results...")

    r = requests.get(URL, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")

    table = soup.find("table")
    if not table:
        raise RuntimeError("Could not find results table on page.")

    rows = table.find("tbody").find_all("tr")

    data = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 8:
            continue

        date_str = cols[1].get_text(strip=True)
        balls = []
        for c in cols[2:8]:
            try:
                balls.append(int(c.get_text(strip=True)))
            except ValueError:
                balls.append(None)

        if None in balls:
            continue

        data.append([date_str] + balls)

    df = pd.DataFrame(data, columns=["date", "b1", "b2", "b3", "b4", "b5", "b6"])
    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y", errors="coerce")
    df = df.dropna(subset=["date"])
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    os.makedirs("data", exist_ok=True)
    out_path = os.path.join("data", "megasena.csv")
    df.to_csv(out_path, index=False, encoding="utf-8")

    print(f"Saved {len(df)} draws to {out_path}")

if __name__ == "__main__":
    fetch_megasena()
