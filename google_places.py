import json
import requests
import populartimes as pt


class GooglePlaces(object):
    def __init__(self, api_key):
        super(GooglePlaces, self).__init__()
        self.api_key = api_key

    def search_places_by_coordinate(self, location, radius, types):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            'key': self.api_key,
            'location': location,
            'radius': radius,
            'types': types
        }
        res = requests.get(endpoint_url, params=params)
        results = json.loads(res.content)
        return results['results']

    def find_place(self, search_input, input_type, fields):
        url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        params = {
            'key': self.api_key,
            'input': search_input,
            'inputtype': input_type,
            'fields': ",".join(fields)
        }
        res = requests.get(url, params=params)
        results = json.loads(res.content)
        return results['candidates']

    def get_place_details(self, place_id, fields):
        url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'key': self.api_key,
            'place_id': place_id,
            'fields': ",".join(fields)
        }
        res = requests.get(url, params=params)
        result = json.loads(res.content)
        return result['result']

    def distance_matrix(self, origin_place_id, destination_place_id):
        url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            'key': self.api_key,
            'origins': 'place_id:' + origin_place_id,
            'destinations': 'place_id:' + destination_place_id
        }
        res = requests.get(url, params=params)
        result = json.loads(res.content)
        return result

    def time_spent(self, place_id):
        result = pt.get_id(self.api_key, place_id)
        return result['time_spent']
