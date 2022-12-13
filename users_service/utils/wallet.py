import requests


class Wallet:
    def __init__(self):
        self.url = "https://payment-service-solfonte.cloud.okteto.net/payment/wallet"

    def create_wallet(self, user_id: int):
        body = {"user_id": user_id}
        headers = {"Content-type": "application/json", "Accept": "application/json"}
        requests.post(self.url, json=body, headers=headers)
