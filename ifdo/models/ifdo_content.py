"""
Define and implement the Image FAIR Digital Object (iFDO) specification for the content section.

Classes:
    ImageAnnotationLabel: Represents an image annotation label.
    ImageAnnotationCreator: Represents an image annotation creator.
    AnnotationLabel: Represents an annotation label with metadata.
    ImageAnnotation: Represents an image annotation with coordinates and labels.
"""

from datetime import datetime

from pydantic import BaseModel


class ImageAnnotationLabel(BaseModel):
    """
    Represent an image annotation label.

    This class defines the structure for an image annotation label, typically used in image labeling and
    classification tasks.

    Attributes:
        id (str): A unique identifier for the annotation label.
        name (str): The name or title of the annotation label.
        info (str): Additional information or description of the annotation label.
    """

    id: str
    name: str
    info: str


class ImageAnnotationCreator(BaseModel):
    """
    Create an image annotation object with associated metadata.

    This class represents an image annotation creator, providing a structure to store and manage information related to
    image annotations.

    Attributes:
        id (str): A unique identifier for the annotation creator.
        name (str): The name of the annotation creator.
        type (str): The type or category of the annotation creator.
    """

    id: str
    name: str
    type: str


class AnnotationLabel(BaseModel):
    """
    Represent an annotation label with associated metadata.

    This class models an annotation label used in data labeling tasks. It includes information about the label itself,
    the annotator who created it, the creation timestamp, and an optional confidence score.

    Attributes:
        label (str): The text of the annotation label.
        annotator (str): The identifier or name of the person who created the annotation.
        created_at (datetime | None): The timestamp when the annotation was created. Defaults to None.
        confidence (float | None): A confidence score associated with the annotation, if applicable. Defaults to None.
    """

    label: str
    annotator: str
    created_at: datetime | None = None
    confidence: float | None = None


class ImageAnnotation(BaseModel):
    """
    Represent an image annotation with coordinates, labels, shape, and frames.

    This class encapsulates the properties of an image annotation, which can be used for various computer vision
    tasks such as object detection, segmentation, or tracking. It allows for flexible representation of
    different annotation types, including bounding boxes, polygons, or keypoints.

    Attributes:
        coordinates (list[float] | list[list[float]]): A list of coordinates representing the annotation's
            position. For bounding boxes, it's [x, y, width, height]. For polygons or keypoints, it's a list of
            [x, y] coordinates.
        labels (list[AnnotationLabel]): A list of AnnotationLabel objects associated with this annotation.
        shape (str | None): The shape of the annotation (e.g., "rectangle", "polygon", "point"). Defaults to None.
        frames (list[float] | None): A list of frame numbers or timestamps for video annotations. Defaults to None.
    """

    coordinates: list[float] | list[list[float]]
    labels: list[AnnotationLabel]
    shape: str | None = None
    frames: list[float] | None = None


class ImageContentFields(BaseModel):
    image_entropy: float | None = None
    image_particle_count: int | None = None
    image_average_color: list[int] | None = None
    image_mpeg7_colorlayout: list[float] | None = None
    image_mpeg7_colorstatistics: list[float] | None = None
    image_mpeg7_colorstructure: list[float] | None = None
    image_mpeg7_dominantcolor: list[float] | None = None
    image_mpeg7_edgehistogram: list[float] | None = None
    image_mpeg7_homogenoustexture: list[float] | None = None
    image_mpeg7_stablecolor: list[float] | None = None
    image_annotation_labels: list[ImageAnnotationLabel] | None = None
    image_annotation_creators: list[ImageAnnotationCreator] | None = None
    image_annotations: list[ImageAnnotation] | None = None
