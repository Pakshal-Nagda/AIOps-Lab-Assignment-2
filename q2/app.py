from contextlib import asynccontextmanager
import joblib
import redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

model = None
cache = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, cache
    model = joblib.load("spam_model.joblib")
    cache = redis.Redis(host="cache", port=6379, decode_responses=True)
    yield
    cache.close()
    model = None

app = FastAPI(lifespan=lifespan)

class PredictionRequest(BaseModel):
    text: str

@app.post("/predict")
def predict(request: PredictionRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    cached_label = cache.get(request.text)
    if cached_label is not None:
        return {"label": cached_label}

    prediction = model.predict([request.text])[0]
    cache.setex(request.text, 300, prediction)
    return {"label": prediction}

@app.get("/healthz")
def healthz():
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    if cache is None:
        raise HTTPException(status_code=503, detail="Cache not accessible")
    return {"status": "ok"}
