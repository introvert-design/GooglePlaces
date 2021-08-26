import os
from dotenv import load_dotenv

from data import create_data
from google_places import GooglePlaces

load_dotenv()

API_KEY = os.getenv('API_KEY')


def build_distance_matrix(response):
    """
    Gets the distance value from the response to create the row list.

    :param response: The concatenated response for max_rows origins.
    :type response: dict

    :return: The distance matrix for max_rows origins.
    :rtype: list
    """
    distance_matrix = []
    for row in response['rows']:
        row_list = [row['elements'][j]['distance']['value'] for j in range(len(row['elements']))]
        distance_matrix.append(row_list)
    return distance_matrix


def merge_responses(responses, length):
    """
    Concatenate the responses for a place.

    :param responses: The responses received for max_rows origin for all destinations.
    :type responses: list[dict]

    :param length: The number of origins in each request.
    :type length: int

    :return: The concatenated response for max_rows origins.
    :rtype: dict
    """
    rows = []
    for row in range(length):
        elements = []
        for response in responses:
            elements.extend(response['rows'][row]['elements'])
        res = {'elements': elements}
        rows.append(res)

    response = {
        'rows': rows
    }
    return response


def send_request(origin, destination):
    """
    Build and send request for the given origin and destination addresses.

    :param origin: The list of place_ids to be treated as origins in one request.
    :type origin: list

    :param destination: The list of place_ids to be treated as destinations in one request.
    :type destination: list

    :return: The response from the distance matrix api.
    :rtype: dict
    """
    def build_str(places):
        return '|place_id:'.join(places)  # Build a pipe-separated string of addresses

    api = GooglePlaces(API_KEY)
    origin_str = build_str(origin)
    destination_str = build_str(destination)
    response = api.distance_matrix(origin_str, destination_str)
    return response


def col_itr(place_ids, q_col, r_col, max_rows, max_cols, origin, distance_matrix):
    """
    Send requests returning max_cols columns per request.

    :param place_ids: A list of place_ids.
    :type place_ids: list

    :param q_col: The number of requests to be send, obtaining max_cols columns per request.
    :type q_col: int

    :param r_col: The remaining columns after q_col x max_cols columns.
    :type r_col: int

    :param max_rows: The maximum number of rows obtained per request.
    :type max_rows: int

    :param max_cols: The maximum number of columns obtained per request.
    :type max_cols: int

    :param origin: The list of place_ids to be treated as origins in one request.
    :type origin: list

    :param distance_matrix: The list of distances between nodes returned after previous request.
    :type distance_matrix: list

    :return: Distance matrix
    :rtype: list
    """
    responses = []
    for j in range(q_col):
        destination = place_ids[j * max_cols: (j + 1) * max_cols]
        response = send_request(origin, destination)
        responses.append(response)

    if r_col > 0:
        destination = place_ids[q_col * max_cols: q_col * max_cols + r_col]
        response = send_request(origin, destination)
        responses.append(response)

    res = merge_responses(responses, max_rows)

    distance_matrix += build_distance_matrix(res)

    return distance_matrix


def create_distance_matrix(place_ids):
    """
    Create the distance matrix.
    Method to overcome the usage limits of Distance Matrix Api.

    :param place_ids: A list of place_ids.
    :type place_ids: list

    :return: A list of distances between the nodes.
    :rtype: list
    """
    # Distance Matrix API only accepts 100 elements per request, so get rows in multiple requests.
    max_elements = 100
    num_places = len(place_ids)
    if num_places > 25:
        max_rows = max_elements // 25
        max_cols = 25
    else:
        max_rows = max_elements // num_places
        max_cols = num_places

    q_row, r_row = divmod(num_places, max_rows)
    q_col, r_col = divmod(num_places, max_cols)

    distance_matrix = []
    # Send q requests, returning max_rows rows per request.
    for i in range(q_row):
        origin = place_ids[i * max_rows: (i + 1) * max_rows]

        distance_matrix = col_itr(place_ids, q_col, r_col, max_rows, max_cols, origin, distance_matrix)

    # Get the remaining remaining r rows, if necessary.
    if r_row > 0:
        origin = place_ids[q_row * max_rows: q_row * max_rows + r_row]

        distance_matrix = col_itr(place_ids, q_col, r_col, max_rows, max_cols, origin, distance_matrix)

    return distance_matrix


########
# Main #
########
def distance():
    """
    Entry point of the program
    """
    place_ids = create_data()  # Create the data.
    distance_matrix = create_distance_matrix(place_ids)

    return distance_matrix


if __name__ == '__main__':
    distance()
