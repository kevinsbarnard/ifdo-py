import datetime

import json

from ifdo import iFDO


def test_load():
    with open("tests/ifdo-video-example.json") as file:
        json_data = json.load(file)

    ifdo = iFDO.from_dict(json_data)

    assert ifdo.image_set_header.image_set_name == "SO268 SO268-1_21-1_OFOS SO_CAM-1_Photo_OFOS"
    assert ifdo.image_set_items["SO268-1_21-1_OFOS_SO_CAM-1_20190304_083724.JPG"][1].image_datetime == datetime.datetime(2019, 3, 4, 8, 37, 25)