import requests
from pprint import pprint

URL_SHEETY = "https://api.sheety.co/4d3d011cb60725fa2d6ac98c453fc84f/flightDeals/prices"


class DataManager:
    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=URL_SHEETY)
        excel_data = response.json()
        self.destination_data = excel_data['prices']
        return self.destination_data

    def updated_data(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(url=f"{URL_SHEETY}/{city['id']}", json=new_data)
            print(response.text)



