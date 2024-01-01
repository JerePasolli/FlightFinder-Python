import requests
from flight_data import FlightData
import os
from pprint import pprint

TEQUILA_ENDPOINT = os.environ.get('TEQUILA_ENDPOINT')
TEQUILA_API_KEY = os.environ.get('TEQUILA_API_KEY')


class FlightSearch:

    def __init__(self):
        self.headers = {
            "apikey": TEQUILA_API_KEY,
        }

    def get_destination_code(self, city_name):
        city_params = {
            "term": city_name,
            "location_types": "city"}
        response = requests.get(f"{TEQUILA_ENDPOINT}/locations/query", headers=self.headers,
                                params=city_params)
        response.raise_for_status()
        return response.json()["locations"][0]["code"]

    def check_flights(self, origin_city, iata_code, from_time, to_time):
        params = {
            "fly_from": origin_city,
            "fly_to": iata_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 2,
            "nights_in_dst_to": 10,
            "one_for_city": 1,
            "max_stopovers": 0,
            "adults": 2,
            "curr": "ARS"
        }
        response = requests.get(f"{TEQUILA_ENDPOINT}/v2/search", headers=self.headers, params=params)
        response.raise_for_status()
        try:
            data = response.json()["data"][0]
        except IndexError:
            try:
                params["max_stopovers"] = 1
                response = requests.get(f"{TEQUILA_ENDPOINT}/v2/search", headers=self.headers, params=params)
                response.raise_for_status()
                data = response.json()["data"][0]
                flight_data = FlightData(
                    price=data["price"],
                    origin_city=data["route"][0]["cityFrom"],
                    origin_airport=data["route"][0]["flyFrom"],
                    destination_city=data["route"][0]["cityTo"],
                    destination_airport=data["route"][0]["flyTo"],
                    out_date=data["route"][0]["local_departure"].split("T")[0],
                    return_date=data["route"][1]["local_departure"].split("T")[0],
                    stop_overs=1,
                    via_city=data["route"][0]["cityTo"]
                )
                return flight_data
            except IndexError:
                print(f"No flight found for {iata_code}.")
                return None
        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
            )
        return flight_data
