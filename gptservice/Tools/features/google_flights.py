import os
import json
import serpapi
import json

serpapi_key = os.environ.get('serpapi_key')

class GoogleFlights:
    def __init__(self, **args):
        self.arrival_id = args.get('arrival_id')
        self.departure_id = args.get('departure_id')
        self.outbound_date = args.get('outbound_date')
        self.return_date = args.get('return_date')
    
    def invoke_service(self):
        try:          
            print("Payloads: %s, %s, %s, %s"% (self.departure_id, self.arrival_id, self.outbound_date, self.return_date))
            search = serpapi.GoogleSearch({
                "engine": "google_flights",
                "departure_id": self.departure_id,
                "arrival_id": self.arrival_id,
                "outbound_date": self.outbound_date,
                "return_date": self.return_date,
                "hl": "en",
                "currency": "INR", # "currency": "INR",
                "gl": "in",
                "api_key": os.environ.get('serpapi_key')
            })
            results = search.get_dict()
            products = results.get('best_flights', results)
            return products
        
        except Exception as e:
            print('Error extracting Flight details')
            print(e)
            return