import json
from datetime import datetime

from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from ifdo import iFDO
from ifdo.models import ImageLicense, ImageContext, ImagePI, ImageCreator, ImageData, ImageSetHeader

OUTPUT_PATH = "/tmp/test_ifdo.json"

def test_save():
    ifdo = iFDO(image_set_header=ImageSetHeader(image_set_name="SO268 SO268-1_21-1_OFOS SO_CAM-1_Photo_OFOS",
                                                image_set_uuid="f840644a-fe4a-46a7-9791-e32c211bcbf5",
                                                image_set_handle= "https://hdl.handle.net/20.500.12085/f840644a-fe4a-46a7-9791-e32c211bcbf5"),
                image_set_items={})

    ifdo.image_set_header.image_abstract = "Acquired by camera SO_CAM-1_Photo_OFOS mounted on platform SO_PFM-01_OFOS during project SO268 (event: SO268-1_21-1_OFOS). Navigation data were automatically edited by the MarIQT software (removal of outliers, smoothed and splined to fill time gaps) and linked to the image data by timestamp."
    ifdo.image_set_header.image_copyright = "Copyright (C)"
    ifdo.image_set_header.image_license = ImageLicense(name="CC-BY")
    ifdo.image_set_header.image_context = ImageContext(name="Image context")
    ifdo.image_set_header.image_project = ImageContext(name="Image project")
    ifdo.image_set_header.image_event = ImageContext(name="Image event")
    ifdo.image_set_header.image_platform = ImageContext(name="Image Platform")
    ifdo.image_set_header.image_sensor = ImageContext(name="Image sensor")
    ifdo.image_set_header.image_pi = ImagePI(name="Image PI")
    ifdo.image_set_header.image_creators = [ImageCreator(name="Image creator")]
    ifdo.image_set_header.image_latitude = 10.0
    ifdo.image_set_header.image_longitude = 10.0
    ifdo.image_set_header.image_altitude_meters = 1.0
    ifdo.image_set_header.image_coordinate_reference_system = "WSG84"
    ifdo.image_set_header.image_coordinate_uncertainty_meters = 0.1
    ifdo.image_set_header.image_datetime = datetime(2020, 1, 1)

    image = ImageData()
    image.image_handle = "test"
    image.image_hash_sha256 = "83f30eb35d1325c44c85fba0cf478825c0a629d20177a945069934f6cd07e087"
    image.image_uuid = "c6b8d981-05c7-449f-85a9-906ab866bfb6"
    image.image_datetime = datetime(2020, 1, 1)
    ifdo.image_set_items["SO268-1_21-1_OFOS_SO_CAM-1_20190304_083724.JPG"] = [image]

    result = ifdo.to_dict()

    schema = load_json("tests/schema/ifdo-v2.1.0.json")

    registry = Registry().with_resources(
        [
            (
                "https://marine-imaging.com/fair/schemas/provenance.json",
                Resource.from_contents(load_json("tests/schema/provenance-v0.1.0.json")),
            ),
            (
                "https://marine-imaging.com/fair/schemas/annotation.json",
                Resource.from_contents(load_json("tests/schema/annotation-v2.0.0.json")),
            ),
        ]
    )
    validator = Draft202012Validator(schema, registry=registry)
    validator.validate(result)

def load_json(filepath: str) -> dict:
    with open(filepath, "r") as file:
        return json.load(file)