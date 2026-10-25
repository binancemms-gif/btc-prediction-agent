"""
Starter FastAPI app for BTC short-term prediction agent.
"""
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="BTC Prediction Agent")

@app.get("/")
async def root():
    return {"message": "BTC Prediction Agent", "status": "starter"}

@app.get("/predict")
async def predict(timeframe: str = "5min"):
    # Placeholder logic - expand with live price + momentum analysis
    return {
        "timeframe": timeframe,
        "prediction": "Down",  # replace with real analysis
        "confidence": 0.55,
        "price_range": "80.4k-80.5k",
        "notes": "Range-bound, mild downside lean. Not financial advice."
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
