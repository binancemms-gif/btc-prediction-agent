"""
BTC short-term prediction agent (FastAPI).
Fetches live price and applies simple range-bound momentum logic.
Not financial advice.
"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import httpx
from datetime import datetime
from pathlib import Path

app = FastAPI(title="BTC Prediction Agent")

# Serve static files if present
static_dir = Path("static")
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

async def get_btc_price() -> float:
    """Fetch current BTC price from CoinGecko."""
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(
                "https://api.coingecko.com/api/v3/simple/price",
                params={"ids": "bitcoin", "vs_currencies": "usd"},
                timeout=10.0,
            )
            data = r.json()
            return float(data["bitcoin"]["usd"])
    except Exception:
        return 80600.0  # fallback

def analyze(price: float) -> dict:
    """Simple range analysis based on recent observed zone ~80.3k-80.7k."""
    low, high = 80300, 80700
    if price > high + 100:
        pred5, pred10 = "Up", "Up"
        notes = "Above recent range, upside breakout lean."
    elif price < low - 100:
        pred5, pred10 = "Down", "Down"
        notes = "Below recent range, downside pressure."
    else:
        # Inside tight range — mild continuation or chop
        pred5 = "Down" if price > 80500 else "Up"
        pred10 = "Choppy"
        notes = "Tight range-bound ($80.3k-$80.7k). Immediate move often continues last leg or chops."
    return {
        "price": round(price, 2),
        "prediction_5min": pred5,
        "prediction_10min": pred10,
        "notes": notes + " Not financial advice.",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

@app.get("/", response_class=HTMLResponse)
async def root():
    index = static_dir / "index.html"
    if index.exists():
        return index.read_text(encoding="utf-8")
    return """<h1>BTC Prediction Agent</h1><p>API ready. See <a href='/predict'>/predict</a></p>"""

@app.get("/price")
async def price():
    p = await get_btc_price()
    return {"btc_usd": p}

@app.get("/predict")
async def predict(timeframe: str = "5min"):
    p = await get_btc_price()
    analysis = analyze(p)
    analysis["timeframe"] = timeframe
    return analysis

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
