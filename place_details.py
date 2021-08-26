from data import create_data
from google_places import GooglePlaces

API_KEY = "AIzaSyBCBBWruaj8M_JC-kfjWEhQZp7ZgdfWw5g"


def places():
    place_ids = create_data()
    fields = ['formatted_address',
              'geometry',
              'name',
              'place_id',
              'type',
              'international_phone_number',
              'opening_hours',
              'website',
              'price_level',
              'rating']
    api = GooglePlaces(API_KEY)
    place_details_list = []
    for place_id in place_ids:
        place = {'google_id': place_id}
        place_details = api.get_place_details(place_id, fields)
        place['place_name'] = place_details['name']
        place['location'] = place_details['geometry']['location']
        place['address'] = place_details['formatted_address']
        place['category'] = place_details['types']

        try:
            place['price_level'] = place_details['price_level']
        except KeyError:
            place['price_level'] = ''

        try:
            place['phone_number'] = place_details['international_phone_number']
        except KeyError:
            place['phone_number'] = ''

        try:
            place['website'] = place_details['website']
        except KeyError:
            place['website'] = ''

        try:
            place['rating'] = place_details['rating']
        except KeyError:
            place['rating'] = ''

        try:
            place['entry'] = place_details['opening_hours']['weekday_text']
        except KeyError:
            place['entry'] = ''

        place_details_list.append(place)
    return place_details_list


if __name__ == '__main__':
    places()
