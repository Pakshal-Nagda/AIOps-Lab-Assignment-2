import time
import requests

URL = "http://localhost:8000/predict"

print("Spam detector started.")
print("Enter a sentence to classify.")
print("Press Ctrl+C to exit.\n")

while True:
    try:
        text = input("Enter text: ")
        if not text.strip():
            continue
        start = time.perf_counter()
        response = requests.post(URL, json={"text": text})
        elapsed = time.perf_counter() - start
        response.raise_for_status()
        result = response.json()
        print(f"Prediction : {result['label']}")
        print(f"Time taken : {elapsed * 1000:.2f} ms\n")

    except KeyboardInterrupt:
        print("\nExiting...")
        break

    except requests.RequestException as e:
        print(f"Request failed: {e}\n")
