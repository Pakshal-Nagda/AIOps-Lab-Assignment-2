FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN python generate_data.py
ENTRYPOINT ["python", "validate.py"]
