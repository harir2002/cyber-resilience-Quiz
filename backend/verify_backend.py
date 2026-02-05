
import requests
import sys
import time

URL = "http://localhost:8001/api/config"

print(f"Checking connection to {URL}...")
try:
    response = requests.get(URL, timeout=2)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("[SUCCESS] Backend is connected and serving config on port 8001!")
        print("Data:", response.json().get("app_title"))
    elif response.status_code == 404:
        print("[FAILURE] Backend is running but returned 404 (Not Found).")
    else:
        print(f"[WARNING] Backend returned unexpected status: {response.status_code}")
except requests.exceptions.ConnectionError:
    print("[FAILURE] Could not connect to backend (Connection Refused).")
    print("The backend is NOT running. Please run 'python main.py'.")
except Exception as e:
    print(f"[ERROR] {e}")
