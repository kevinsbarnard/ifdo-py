from tempfile import NamedTemporaryFile

import yaml
import json

from ifdo import iFDO


def test_load():
    with open("tests/ifdo-video-example.json") as file:
        json_data = json.load(file)

    file = NamedTemporaryFile("w")
    file.write(yaml.safe_dump(json_data))
    file.flush()
    ifdo = iFDO.load(file.name)
    file.close()

    assert ifdo.image_set_header.image_set_name == "SO268 SO268-1_21-1_OFOS SO_CAM-1_Photo_OFOS"
    assert ifdo.image_set_items["SO268-1_21-1_OFOS_SO_CAM-1_20190304_083724.JPG"][1].image_datetime == "2019-03-04 08:37:25.000000"
