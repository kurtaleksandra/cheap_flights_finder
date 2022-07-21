#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()


if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_iata_code(row["city"])
    data_manager.destination_data = sheet_data
    data_manager.updated_data()


DEPARTURE_CITY = "LON"
TOMORROW = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
SIX_MONTHS = (datetime.now() + timedelta(days=180)).strftime("%d/%m/%Y")

for destination in sheet_data:
    flight = flight_search.get_price_data(
        departure_city_code=DEPARTURE_CITY,
        destination_city_code=destination["iataCode"],
        from_time=TOMORROW,
        to_time=SIX_MONTHS
    )

    if flight is None:
        continue

    if flight.price < destination["lowestPrice"]:
            message = f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."
            if flight.stop_overs > 0:
                message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."

            notification_manager.send_sms(message)








