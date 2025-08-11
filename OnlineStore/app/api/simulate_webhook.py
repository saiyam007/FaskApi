import os
import hmac
import hashlib
import json
import requests

BASE_URL = "http://localhost:8000"
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "dev-secret")

# === Step 1: Create Product ===
product_data = {
    "sku": "SKU-TEST",
    "name": "Webhook Test Product",
    "price": 10.00,
    "stock": 5
}
resp = requests.post(f"{BASE_URL}/products", json=product_data)
resp.raise_for_status()
product_id = resp.json()["id"]
print(f"[+] Product created: {product_id}")

# === Step 2: Create Order ===
order_data = {
    "product_id": product_id,
    "quantity": 1
}
resp = requests.post(f"{BASE_URL}/orders", json=order_data)
resp.raise_for_status()
order_id = resp.json()["id"]
print(f"[+] Order created: {order_id}")

# === Step 3: Prepare Webhook Payload ===
payload = {
    "event": "payment.succeeded",
    "data": {"order_id": order_id}
}
payload_bytes = json.dumps(payload).encode()

# === Step 4: Generate HMAC Signature ===
signature = hmac.new(
    WEBHOOK_SECRET.encode(),
    payload_bytes,
    hashlib.sha256
).hexdigest()

# === Step 5: Send Webhook ===
headers = {
    "Content-Type": "application/json",
    "X-Payment-Signature": signature
}
resp = requests.post(f"{BASE_URL}/webhooks/payment", headers=headers, data=json.dumps(payload))
print(f"[+] Webhook response: {resp.status_code} {resp.json()}")

# === Step 6: Verify Order Status ===
resp = requests.get(f"{BASE_URL}/orders/{order_id}")
resp.raise_for_status()
print(f"[+] Final order status: {resp.json()['status']}")
