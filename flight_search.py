import requests
from flight_data import FlightData
from pprint import pprint


APIKEY = "btfiJ2kw2AdvGTyIv19h-7Ssc_tkIxhl"
KIWI_URL = "https://tequila-api.kiwi.com/locations/query"
KIWI_SEARCH_URL = "https://tequila-api.kiwi.com/v2/search"
HEADERS = {"apikey": APIKEY}


class FlightSearch:
    def get_iata_code(self, city_name):
        response = requests.get(url=KIWI_URL, params={"term": city_name, "location_types": "city"}, headers=HEADERS)
        result = response.json()["locations"]
        code = result[0]["code"]
        return code

    def get_price_data(self, departure_city_code, destination_city_code, from_time, to_time):
        data_params = {
            "fly_from": departure_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time,
            "date_to": to_time,
            "max_stopovers": "0",
            "curr": "GBP",
            "nights_in_dst_from": "7",
            "nights_in_dst_to": "28",
            "flight_type": "round"}

        response = requests.get(url=KIWI_SEARCH_URL, params=data_params, headers=HEADERS)

        try:
            flight_raw_data = response.json()["data"][0]
        except IndexError:
            data_params["max_stopovers"] = 1
            response = requests.get(
                url=KIWI_SEARCH_URL,
                headers=HEADERS,
                params=data_params,

            )
            flight_raw_data = response.json()["data"][0]
            pprint(flight_raw_data)
            flight_data = FlightData(
                price=flight_raw_data["price"],
                origin_city=flight_raw_data["route"][0]["cityFrom"],
                origin_airport=flight_raw_data["route"][0]["flyFrom"],
                destination_city=flight_raw_data["route"][1]["cityTo"],
                destination_airport=flight_raw_data["route"][1]["flyTo"],
                out_date=flight_raw_data["route"][0]["local_departure"].split("T")[0],
                return_date=flight_raw_data["route"][2]["local_departure"].split("T")[0],
                stop_overs=1,
                via_city=flight_raw_data["route"][0]["cityTo"]
            )
            return flight_data
        else:
            flight_data = FlightData(
                price=flight_raw_data["price"],
                origin_city=flight_raw_data["route"][0]["cityFrom"],
                origin_airport=flight_raw_data["route"][0]["flyFrom"],
                destination_city=flight_raw_data["route"][0]["cityTo"],
                destination_airport=flight_raw_data["route"][0]["flyTo"],
                out_date=flight_raw_data["route"][0]["local_departure"].split("T")[0],
                return_date=flight_raw_data["route"][1]["local_departure"].split("T")[0]
            )
            return flight_data




