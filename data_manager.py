import requests
import os

SHEET_ENDPOINT = os.environ.get('SHEET_ENDPOINT')


class DataManager:

    def __init__(self):
        self.sheet_data = {}

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
            response = requests.put(f"{SHEET_ENDPOINT}/{row['id']}", json=new_data)
            response.raise_for_status()
