import requests
import os

SHEET_ENDPOINT = os.environ.get('SHEET_ENDPOINT')
SHEETY_ENDPOINT_USERS = "https://api.sheety.co/03beca8699447bc09f7c0e52123d017e/flightDeals/users"
SHEETY_TOKEN = os.environ.get("SHEETY_TOKEN")


class DataManager:

    def __init__(self):
        self.sheet_data = {}
        self.headers = {
            "Authorization": f"Bearer {SHEETY_TOKEN}",
        }

    def get_sheet_data(self):
        response = requests.get(SHEET_ENDPOINT)
        response.raise_for_status()
        data = response.json()
        self.sheet_data = data["prices"]
        return self.sheet_data

    def update_sheet_data(self, update_type):
        for row in self.sheet_data:
            if update_type == 0:
                new_data = {
                    "price": {
                        "iataCode": row["iataCode"]
                    }
                }
            else:
                new_data = {
                    "price": {
                        "lowestPrice": row["lowestPrice"]
                    }
                }
            response = requests.put(f"{SHEET_ENDPOINT}/{row['id']}", json=new_data, headers=self.headers)
            response.raise_for_status()

    def get_customer_emails(self):
        response = requests.get(SHEETY_ENDPOINT_USERS, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        return data["users"]
