# ---------- Builder stage ----------
FROM python:3.11 AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY generate_data.py .
COPY train.py .
RUN python generate_data.py
RUN python train.py

# ---------- Runtime stage ----------
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local /usr/local
COPY --from=builder /build/spam_model.joblib .
COPY app.py .

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]