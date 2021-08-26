import json


def create_data():
    """
    Gets the place Ids from the json file as a list.
    Change this function to suit the source from which the data is received.

    :return: The list of place_ids
    :rtype: list
    """
    with open("delhi.json", "r") as infile:
        places = json.load(infile)
    return [place for place in places['place_ids']]
