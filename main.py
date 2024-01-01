from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

ORIGIN_CITY = "COR"  # cordoba, argentina

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

sheet_data = data_manager.get_sheet_data()

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])

    data_manager.sheet_data = sheet_data
    data_manager.update_sheet_data(0)

tomorrow = datetime.now() + timedelta(days=1)
twelve_months = datetime.now() + timedelta(days=(12 * 30))

for row in sheet_data:
    flight = flight_search.check_flights(
        ORIGIN_CITY,
        row["iataCode"],
        tomorrow,
        twelve_months
    )

    if flight is None:
        continue

    if flight.price < row["lowestPrice"]:
        users = data_manager.get_customer_emails()
        emails = [row["email"] for row in users]
        names = [row["firstName"] for row in users]

        row["lowestPrice"] = flight.price
        data_manager.sheet_data = sheet_data
        data_manager.update_sheet_data(1)
        message = f"Low price alert! Only ARS${flight.price} to fly from {flight.origin_city}"
        f"-{flight.origin_airport} to {flight.destination_city}-"
        f"{flight.destination_airport}, from {flight.out_date} to "
        f"{flight.return_date}."

        if flight.stop_overs > 0:
            message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."

        notification_manager.send_sms(message)
        notification_manager.send_emails(emails, message)
