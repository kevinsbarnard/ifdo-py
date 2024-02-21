from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

from yaml import safe_dump, safe_load
from ifdo.model import model
from stringcase import spinalcase

ifdo_model = model(case_func=spinalcase)  # Use spinalcase for all field names


class ImageAcquisition(str, Enum):
    PHOTO = "photo"
    VIDEO = "video"
    SLIDE = "slide"


class ImageQuality(str, Enum):
    RAW = "raw"
    PROCESSED = "processed"
    PRODUCT = "product"


class ImageDeployment(str, Enum):
    MAPPING = "mapping"
    STATIONARY = "stationary"
    SURVEY = "survey"
    EXPLORATION = "exploration"
    EXPERIMENT = "experiment"


class ImageNavigation(str, Enum):
    SATELLITE = "satellite"
    BEACON = "beacon"
    TRANSPONDER = "transponder"
    RECONSTRUCTED = "reconstructed"


class ImageScaleReference(str, Enum):
    CAMERA_3D = "3D camera"
    CAMERA_CALIBRATED = "calibrated camera"
    LASER_MARKER = "laser marker"
    OPTICAL_FLOW = "optical flow"


class ImageIllumination(str, Enum):
    SUNLIGHT = "sunlight"
    ARTIFICIAL_LIGHT = "artificial light"
    MIXED_LIGHT = "mixed light"


class ImagePixelMagnitude(str, Enum):
    KM = "km"
    HM = "hm"
    DAM = "dam"
    M = "m"
    CM = "cm"
    MM = "mm"
    UM = "µm"


class ImageMarineZone(str, Enum):
    SEAFLOOR = "seafloor"
    WATER_COLUMN = "water column"
    SEA_SURFACE = "sea surface"
    ATMOSPHERE = "atmosphere"
    LABORATORY = "laboratory"


class ImageSpectralResolution(str, Enum):
    GRAYSCALE = "grayscale"
    RGB = "rgb"
    MULTI_SPECTRAL = "multi-spectral"
    HYPER_SPECTRAL = "hyper-spectral"


class ImageCaptureMode(str, Enum):
    TIMER = "timer"
    MANUAL = "manual"
    MIXED = "mixed"


class ImageFaunaAttraction(str, Enum):
    NONE = "none"
    BAITED = "baited"
    LIGHT = "light"


@ifdo_model
class ImagePI:
    name: str
    orcid: str


@ifdo_model
class ImageAnnotationLabel:
    id: str
    name: str
    info: str


@ifdo_model
class ImageAnnotationCreator:
    id: str
    name: str
    type: str


@ifdo_model
class AnnotationLabel:
    label: str
    annotator: str
    created_at: Optional[datetime] = None
    confidence: Optional[float] = None


@ifdo_model
class ImageAnnotation:
    coordinates: Union[List[float], List[List[float]]]
    labels: List[AnnotationLabel]
    shape: Optional[str] = None
    frames: Optional[List[float]] = None


@ifdo_model
class CameraPose:
    pose_utm_zone: str
    pose_utm_epsg: str
    pose_utm_east_north_up_meters: List[float]
    pose_absolute_orientation_utm_matrix: List[List[float]]


@ifdo_model
class CameraHousingViewport:
    viewport_type: str
    viewport_optical_density: float
    viewport_thickness_millimeter: float
    viewport_extra_description: Optional[str] = None


@ifdo_model
class FlatportParameters:
    flatport_lens_port_distance_millimeter: float
    flatport_interface_normal_direction: Tuple[float, float, float]
    flatport_extra_description: Optional[str] = None


@ifdo_model
class DomeportParameters:
    domeport_outer_radius_millimeter: float
    domeport_decentering_offset_xyz_millimeter: Tuple[float, float, float]
    domeport_extra_description: Optional[str] = None


@ifdo_model
class CameraCalibrationModel:
    calibration_model_type: str
    calibration_focal_length_xy_pixel: Tuple[float, float]
    calibration_principal_point_xy_pixel: Tuple[float, float]
    calibration_distortion_coefficients: List[float]
    calibration_approximate_field_of_view_water_xy_degree: Tuple[float, float]
    calibration_model_extra_description: Optional[str] = None


@ifdo_model
class PhotometricCalibration:
    photometric_sequence_white_balancing: str
    photometric_exposure_factor_RGB: Tuple[float, float, float]
    photometric_sequence_illumination_type: str
    photometric_sequence_illumination_description: str
    photometric_illumination_factor_RGB: Tuple[float, float, float]
    photometric_water_properties_description: str


@ifdo_model
class ImageData:
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
    image_acquisition: Optional[ImageAcquisition] = None
    image_quality: Optional[ImageQuality] = None
    image_deployment: Optional[ImageDeployment] = None
    image_navigation: Optional[ImageNavigation] = None
    image_scale_reference: Optional[ImageScaleReference] = None
    image_illumination: Optional[ImageIllumination] = None
    image_pixel_mag: Optional[ImagePixelMagnitude] = None
    image_marine_zone: Optional[ImageMarineZone] = None
    image_spectral_resolution: Optional[ImageSpectralResolution] = None
    image_capture_mode: Optional[ImageCaptureMode] = None
    image_fauna_attraction: Optional[ImageFaunaAttraction] = None
    image_area_square_meter: Optional[float] = None
    image_meters_above_ground: Optional[float] = None
    image_acquisition_settings: Optional[dict] = None
    image_camera_yaw_degrees: Optional[float] = None
    image_camera_pitch_degrees: Optional[float] = None
    image_camera_roll_degrees: Optional[float] = None
    image_overlap_fraction: Optional[float] = None
    image_datetime_format: Optional[str] = None
    image_camera_pose: Optional[CameraPose] = None
    image_camera_housing_viewport: Optional[CameraHousingViewport] = None
    image_flatport_parameters: Optional[FlatportParameters] = None
    image_domeport_parameters: Optional[DomeportParameters] = None
    image_camera_calibration_model: Optional[CameraCalibrationModel] = None
    image_photometric_calibration: Optional[PhotometricCalibration] = None
    image_objective: Optional[str] = None
    image_target_environment: Optional[str] = None
    image_target_timescale: Optional[str] = None
    image_spatial_constraints: Optional[str] = None
    image_temporal_constraints: Optional[str] = None
    image_time_synchronization: Optional[str] = None
    image_item_identification_scheme: Optional[str] = None
    image_curation_protocol: Optional[str] = None
    
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


@ifdo_model
class ImageSetHeader:
    image_set_name: str
    image_set_uuid: str
    image_set_handle: str
    image_set_ifdo_version: str = "v1.0.0"
    
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
    image_acquisition: Optional[ImageAcquisition] = None
    image_quality: Optional[ImageQuality] = None
    image_deployment: Optional[ImageDeployment] = None
    image_navigation: Optional[ImageNavigation] = None
    image_scale_reference: Optional[ImageScaleReference] = None
    image_illumination: Optional[ImageIllumination] = None
    image_pixel_mag: Optional[ImagePixelMagnitude] = None
    image_marine_zone: Optional[ImageMarineZone] = None
    image_spectral_resolution: Optional[ImageSpectralResolution] = None
    image_capture_mode: Optional[ImageCaptureMode] = None
    image_fauna_attraction: Optional[ImageFaunaAttraction] = None
    image_area_square_meter: Optional[float] = None
    image_meters_above_ground: Optional[float] = None
    image_acquisition_settings: Optional[dict] = None
    image_camera_yaw_degrees: Optional[float] = None
    image_camera_pitch_degrees: Optional[float] = None
    image_camera_roll_degrees: Optional[float] = None
    image_overlap_fraction: Optional[float] = None
    image_datetime_format: Optional[str] = None
    image_camera_pose: Optional[CameraPose] = None
    image_camera_housing_viewport: Optional[CameraHousingViewport] = None
    image_flatport_parameters: Optional[FlatportParameters] = None
    image_domeport_parameters: Optional[DomeportParameters] = None
    image_camera_calibration_model: Optional[CameraCalibrationModel] = None
    image_photometric_calibration: Optional[PhotometricCalibration] = None
    image_objective: Optional[str] = None
    image_target_environment: Optional[str] = None
    image_target_timescale: Optional[str] = None
    image_spatial_constraints: Optional[str] = None
    image_temporal_constraints: Optional[str] = None
    image_time_synchronization: Optional[str] = None
    image_item_identification_scheme: Optional[str] = None
    image_curation_protocol: Optional[str] = None
    
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


@ifdo_model
class iFDO:
    image_set_header: ImageSetHeader
    image_set_items: Dict[str, List[ImageData]]
    
    @classmethod
    def load(cls, path: Union[str, Path]) -> 'iFDO':
        """
        Load an iFDO from a YAML file.
        
        Args:
            path: Path to the YAML file.
        
        Returns:
            The loaded iFDO object.
        """
        path = Path(path)  # Ensure Path object
        with path.open() as f:
            d = safe_load(f)
        return cls.from_dict(d)
    
    def save(self, path: Union[str, Path]) -> None:
        """
        Save to a YAML file.
        
        Args:
            path: Path to the YAML file.
        """
        path = Path(path)  # Ensure Path object
        with path.open('w') as f:
            safe_dump(self.to_dict(), f, sort_keys=False)
