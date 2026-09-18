from contextlib import asynccontextmanager
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    model = joblib.load("spam_model.joblib")
    yield
    model = None

app = FastAPI(lifespan=lifespan)

class PredictionRequest(BaseModel):
    text: str

@app.post("/predict")
def predict(request: PredictionRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    prediction = model.predict([request.text])[0]
    return {"label": prediction}

@app.get("/healthz")
def healthz():
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "ok"}
