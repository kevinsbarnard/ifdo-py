from datetime import datetime
from typing import Dict, List, Optional
from ifdo.dto import dto
from stringcase import spinalcase

ifdo_dto = dto(case_func=spinalcase)  # Use spinalcase for all field names


@ifdo_dto
class ImagePI:
    name: str
    orcid: str


@ifdo_dto
class ImageAnnotationLabel:
    id: str
    name: str
    info: str


@ifdo_dto
class ImageAnnotationCreator:
    id: str
    name: str
    type: str


@ifdo_dto
class AnnotationCoordinate:
    x: float
    y: float


@ifdo_dto
class AnnotationLabel:
    id: str
    annotator: str
    created_at: datetime
    confidence: float


@ifdo_dto
class ImageAnnotation:
    coordinates: List[AnnotationCoordinate]
    labels: List[AnnotationLabel]
    shape: str
    frames: Optional[List[float]] = None


@ifdo_dto
class ImageSetItem:
    # iFDO core (required)
    image_datetime: Optional[datetime] = None
    image_latitude: Optional[float] = None
    image_longitude: Optional[float] = None
    image_depth: Optional[float] = None
    image_altitude: Optional[float] = None
    image_coordinate_reference_system: Optional[str] = None
    image_coordinate_uncertainty_meters: Optional[float] = None
    image_context: Optional[str] = None
    image_project: Optional[str] = None
    image_event: Optional[str] = None
    image_platform: Optional[str] = None
    image_sensor: Optional[str] = None
    image_uuid: Optional[str] = None
    image_hash_sha256: Optional[str] = None
    image_pi: Optional[ImagePI] = None
    image_creators: Optional[List[ImagePI]] = None
    image_license: Optional[str] = None
    image_copyright: Optional[str] = None
    image_abstract: Optional[str] = None
    
    # iFDO capture (optional)
    image_acquisition: Optional[str] = None
    image_quality: Optional[str] = None
    image_deployment: Optional[str] = None
    image_navigation: Optional[str] = None
    image_scale_reference: Optional[str] = None
    image_illumination: Optional[str] = None
    image_pixel_mag: Optional[str] = None
    image_marine_zone: Optional[str] = None
    image_spectral_resolution: Optional[str] = None
    image_capture_mode: Optional[str] = None
    image_fauna_attraction: Optional[str] = None
    
    # iFDO content (optional)
    image_entropy: Optional[float] = None
    image_particle_count: Optional[int] = None
    image_average_color: Optional[List[int]] = None
    image_mpeg7_colorlayout: Optional[List[float]] = None
    image_mpeg7_colorstatistics: Optional[List[float]] = None
    image_mpeg7_colorstructure: Optional[List[float]] = None
    image_mpeg7_dominantcolor: Optional[List[float]] = None
    image_mpeg7_edgehistogram: Optional[List[float]] = None
    image_mpeg7_homogenoustexture: Optional[List[float]] = None
    image_mpeg7_stablecolor: Optional[List[float]] = None
    image_annotation_labels: Optional[List[ImageAnnotationLabel]] = None
    image_annotation_creators: Optional[List[ImageAnnotationCreator]] = None
    image_annotations: Optional[List[ImageAnnotation]] = None


@ifdo_dto
class ImageSetHeader:
    image_set_name: str
    image_set_uuid: str
    image_set_handle: str
    image_set_ifdo_version: Optional[str] = None
    image_datetime: Optional[datetime] = None
    image_latitude: Optional[float] = None
    image_longitude: Optional[float] = None
    image_depth: Optional[float] = None
    image_altitude: Optional[float] = None
    image_coordinate_reference_system: Optional[str] = None
    image_coordinate_uncertainty_meters: Optional[float] = None
    image_context: Optional[str] = None
    image_project: Optional[str] = None
    image_event: Optional[str] = None
    image_platform: Optional[str] = None
    image_sensor: Optional[str] = None
    image_uuid: Optional[str] = None
    image_hash_sha256: Optional[str] = None
    image_pi: Optional[ImagePI] = None
    image_creators: Optional[List[ImagePI]] = None
    image_license: Optional[str] = None
    image_copyright: Optional[str] = None
    image_abstract: Optional[str] = None


@ifdo_dto
class iFDO:
    image_set_header: ImageSetHeader
    image_set_items: Dict[str, ImageSetItem]
