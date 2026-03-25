from math import asin, cos, radians, sin, sqrt

import pandas as pd


def haversine(lat1, lon1, lat2, lon2):

    R = 6371

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    )
    c = 2 * asin(sqrt(a))

    return R * c


def find_nearest_ambulance(lat, lon):

    ambulances = pd.read_csv("data/ambulance_locations.csv")

    ambulances = ambulances[ambulances["available"] == 1]

    distances = []

    for _, amb in ambulances.iterrows():

        d = haversine(lat, lon, amb["lat"], amb["lon"])

        distances.append(d)

    ambulances["distance"] = distances

    nearest = ambulances.sort_values("distance").iloc[0]

    eta = (nearest["distance"] / 40) * 60

    return nearest["ambulance_id"], nearest["distance"], eta
