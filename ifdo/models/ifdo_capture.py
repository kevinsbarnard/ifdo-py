"""
Define and implement the Image FAIR Digital Object (iFDO) specification for the capture section.

Classes:
    ImageAcquisition: Enumeration for image acquisition types.
    ImageQuality: Enumeration for image quality levels.
    ImageDeployment: Enumeration for image deployment strategies.
    ImageNavigation: Enumeration for image navigation types.
    ImageScaleReference: Enumeration for image scale reference types.
    ImageIllumination: Enumeration for types of image illumination.
    ImagePixelMagnitude: Enumeration for image pixel magnitude units.
    ImageMarineZone: Enumeration for different marine zones.
    ImageSpectralResolution: Enumeration for image spectral resolution types.
    ImageCaptureMode: Enumeration for image capture modes.
    ImageFaunaAttraction: Enumeration for image fauna attraction types.
    ImageCameraPose: Represents a camera pose with UTM coordinates and orientation.
    ImageCameraHousingViewport: Represents a camera housing viewport.
    ImageFlatportParameters: Defines parameters for a flatport in an optical system.
    ImageDomeportParameters: Defines parameters for a domeport in an optical system.
    ImageCameraCalibrationModel: Defines a camera calibration model.
    ImagePhotometricCalibration: Represents photometric calibration parameters.
"""

from enum import Enum
from typing import Any

from pydantic import BaseModel


class ImageAcquisition(str, Enum):
    """Define an enumeration for image acquisition types.

    This class represents different methods of image acquisition in a photography or imaging context.

    Attributes:
        PHOTO (str): Represents image acquisition through a still photograph.
        VIDEO (str): Represents image acquisition through video recording.
        SLIDE (str): Represents image acquisition through a slide: microscopy images / slide scans.
    """

    PHOTO = "photo"
    VIDEO = "video"
    SLIDE = "slide"


class ImageQuality(str, Enum):
    """
    Define an enumeration for image quality levels.

    This class represents different levels of image quality used in image processing or storage.

    Attributes:
        RAW: Represents raw, unprocessed image quality.
        PROCESSED: Represents processed image quality, typically after some form of enhancement or modification.
        PRODUCT: Represents final product image quality, suitable for end-user consumption or display.
    """

    RAW = "raw"
    PROCESSED = "processed"
    PRODUCT = "product"


class ImageDeployment(str, Enum):
    """
    Enumerate different types of image deployment strategies.

    This class is an enumeration that defines various types of image deployment strategies used in different
    scenarios.

    Attributes:
        MAPPING (str): Planned path execution along 2-3 spatial axes.
        STATIONARY (str): Fixed spatial position.
        SURVEY (str): Planned path execution along free path.
        EXPLORATION (str): Unplanned path execution.
        EXPERIMENT (str): Observation of manipulated environment.
        SAMPLING (str): Ex-situ imaging of samples taken by other method.
    """

    MAPPING = "mapping"
    STATIONARY = "stationary"
    SURVEY = "survey"
    EXPLORATION = "exploration"
    EXPERIMENT = "experiment"
    SAMPLING = "sampling"


class ImageNavigation(str, Enum):
    """Define image navigation types for spatial coordinates.

    This enumeration class provides a set of predefined constants representing different types of image navigation
    techniques used to capture image spatial coordinates.

    Attributes:
        SATELLITE: Represents navigation using satellite imagery.
        BEACON: Represents navigation using beacon signals.
        TRANSPONDER: Represents navigation using transponder signals.
        RECONSTRUCTED: Represents navigation using reconstructed coordinates.
    """

    SATELLITE = "satellite"
    BEACON = "beacon"
    TRANSPONDER = "transponder"
    RECONSTRUCTED = "reconstructed"


class ImageScaleReference(str, Enum):
    """
    Define an enumeration for image scale reference types.

    This class defines an enumeration of different image scale reference types used in computer vision and
    image processing applications.

    Attributes:
        CAMERA_3D (str): Represents a 3D camera as the scale reference.
        CAMERA_CALIBRATED (str): Represents a calibrated camera as the scale reference.
        LASER_MARKER (str): Represents a laser marker as the scale reference.
        OPTICAL_FLOW (str): Represents optical flow as the scale reference.
    """

    CAMERA_3D = "3D camera"
    CAMERA_CALIBRATED = "calibrated camera"
    LASER_MARKER = "laser marker"
    OPTICAL_FLOW = "optical flow"


class ImageIllumination(str, Enum):
    """
    Define an enumeration for types of image illumination.

    This class represents different types of illumination conditions that can be present in an image. The class provides
    three predefined illumination types: sunlight, artificial light, and mixed light.

    Attributes:
        SUNLIGHT (str): Represents illumination from natural sunlight.
        ARTIFICIAL_LIGHT (str): Represents illumination from artificial light sources.
        MIXED_LIGHT (str): Represents a combination of natural and artificial light sources.
    """

    SUNLIGHT = "sunlight"
    ARTIFICIAL_LIGHT = "artificial light"
    MIXED_LIGHT = "mixed light"


class ImagePixelMagnitude(str, Enum):
    """
    Define image pixel magnitude units as an enumeration.

    This class represents different units of measurement for image pixel magnitudes.

    Attributes:
        KM (str): Kilometer unit, represented as 'km'.
        HM (str): Hectometer unit, represented as 'hm'.
        DAM (str): Decameter unit, represented as 'dam'.
        M (str): Meter unit, represented as 'm'.
        CM (str): Centimeter unit, represented as 'cm'.
        MM (str): Millimeter unit, represented as 'mm'.
        UM (str): Micrometer unit, represented as 'µm'.
    """

    KM = "km"
    HM = "hm"
    DAM = "dam"
    M = "m"
    CM = "cm"
    MM = "mm"
    UM = "µm"


class ImageMarineZone(str, Enum):
    """
    Define an enumeration for different marine zones.

    This class represents various marine zones im which images are captured.

    Attributes:
        SEAFLOOR (str): Represents the seafloor zone.
        WATER_COLUMN (str): Represents the water column zone.
        SEA_SURFACE (str): Represents the sea surface zone.
        ATMOSPHERE (str): Represents the atmosphere zone above the sea surface.
        LABORATORY (str): Represents images taken in a laboratory setting.
    """

    SEAFLOOR = "seafloor"
    WATER_COLUMN = "water column"
    SEA_SURFACE = "sea surface"
    ATMOSPHERE = "atmosphere"
    LABORATORY = "laboratory"


class ImageSpectralResolution(str, Enum):
    """
    Define an enumeration for image spectral resolution types.

    This class provides an enumeration of different image spectral resolution types commonly used in image processing
    and remote sensing.

    Attributes:
        GRAYSCALE (str): Represents grayscale images with a single channel.
        RGB (str): Represents RGB (Red, Green, Blue) images with three channels.
        MULTI_SPECTRAL (str): Represents multi-spectral images with typically 4-10 spectral bands.
        HYPER_SPECTRAL (str): Represents hyper-spectral images with 10+ spectral bands.
    """

    GRAYSCALE = "grayscale"
    RGB = "rgb"
    MULTI_SPECTRAL = "multi-spectral"
    HYPER_SPECTRAL = "hyper-spectral"


class ImageCaptureMode(str, Enum):
    """
    Define an enumeration for image capture modes.

    This class represents different modes of image capture in a photography or imaging application.

    Attributes:
        TIMER (str): Represents a timer-based image capture mode.
        MANUAL (str): Represents a manual image capture mode.
        MIXED (str): Represents a mixed mode combining timer and manual capture.
    """

    TIMER = "timer"
    MANUAL = "manual"
    MIXED = "mixed"


class ImageFaunaAttraction(str, Enum):
    """
    Define an enumeration for image fauna attraction types.

    This class represents different types of attraction methods used for camera systems to capture images of fauna.

    Attributes:
        NONE (str): Indicates no specific attraction method used.
        BAITED (str): Indicates the use of bait to attract fauna.
        LIGHT (str): Indicates the use of light to attract fauna.
    """

    NONE = "none"
    BAITED = "baited"
    LIGHT = "light"


class ImageCameraPose(BaseModel):
    """
    Represent a camera pose with UTM coordinates and orientation.

    This class encapsulates information about a camera's position and orientation in a Universal Transverse Mercator
    (UTM) coordinate system. It includes the UTM zone, EPSG code, East-North-Up coordinates, and the absolute
    orientation matrix.

    Attributes:
        pose_utm_zone (str): The UTM zone identifier for the camera's location.
        pose_utm_epsg (str): The EPSG code for the specific UTM coordinate reference system.
        pose_utm_east_north_up_meters (list[float]): A list of three floats representing the East, North, and Up
            coordinates in meters.
        pose_absolute_orientation_utm_matrix (list[list[float]]): A 3x3 or 4x4 matrix represented as a list of lists,
            describing the camera's absolute orientation in the UTM coordinate system.
    """

    pose_utm_zone: str
    pose_utm_epsg: str
    pose_utm_east_north_up_meters: list[float]
    pose_absolute_orientation_utm_matrix: list[list[float]]


class ImageCameraHousingViewport(BaseModel):
    """
    Represent a camera housing viewport with its properties.

    This class models a viewport used in underwater camera housings. It captures essential characteristics
    such as the type of viewport, its optical density, thickness, and any additional descriptive information.

    Attributes:
        viewport_type (str): The type of viewport material or design.
        viewport_optical_density (float): The optical density of the viewport material.
        viewport_thickness_millimeter (float): The thickness of the viewport in millimeters.
        viewport_extra_description (str | None): Additional description or notes about the viewport. Defaults to None.
    """

    viewport_type: str
    viewport_optical_density: float
    viewport_thickness_millimeter: float
    viewport_extra_description: str | None = None


class ImageFlatportParameters(BaseModel):
    """
    Define parameters for a flatport in an optical system.

    This class encapsulates the parameters required to define a flatport in an optical system. It includes
    attributes for specifying the distance between the flatport and the lens port, the normal direction of the
    flatport interface, and an optional extra description.

    Attributes:
        flatport_lens_port_distance_millimeter (float): The distance between the flatport and the lens port in
            millimeters.
        flatport_interface_normal_direction (tuple[float, float, float]): A tuple representing the normal
            direction of the flatport interface in 3D space.
        flatport_extra_description (str | None): An optional string providing additional information about the
            flatport. Defaults to None.
    """

    flatport_lens_port_distance_millimeter: float
    flatport_interface_normal_direction: tuple[float, float, float]
    flatport_extra_description: str | None = None


class ImageDomeportParameters(BaseModel):
    """
    Define parameters for a domeport in an optical system.

    This class represents the parameters of a domeport, which is a component in optical systems used to protect
    cameras or sensors in underwater or extreme environments. It captures essential geometric properties and
    additional descriptive information about the domeport.

    Attributes:
        domeport_outer_radius_millimeter (float): The outer radius of the domeport in millimeters.
        domeport_decentering_offset_xyz_millimeter (tuple[float, float, float]): The x, y, and z offsets of the
            domeport's center from the optical axis, in millimeters.
        domeport_extra_description (str | None): Optional additional description or notes about the domeport.
            Defaults to None.
    """

    domeport_outer_radius_millimeter: float
    domeport_decentering_offset_xyz_millimeter: tuple[float, float, float]
    domeport_extra_description: str | None = None


class ImageCameraCalibrationModel(BaseModel):
    """
    Define a camera calibration model with intrinsic parameters and distortion coefficients.

    This class represents a camera calibration model, containing essential parameters for camera calibration
    such as focal length, principal point, and distortion coefficients. It also includes additional information
    like the calibration model type and approximate field of view in water. The class is decorated with @ifdo_model,
    which may provide additional functionality or validation.

    Attributes:
        calibration_model_type (str): The type or name of the calibration model used.
        calibration_focal_length_xy_pixel (tuple[float, float]): The focal length in pixels for x and y directions.
        calibration_principal_point_xy_pixel (tuple[float, float]): The principal point coordinates in pixels.
        calibration_distortion_coefficients (list[float]): List of distortion coefficients for the camera model.
        calibration_approximate_field_of_view_water_xy_degree (tuple[float, float]): Approximate field of view in water
            for x and y directions, measured in degrees.
        calibration_model_extra_description (str | None): Additional description or notes about the calibration model.
            Defaults to None.
    """

    calibration_model_type: str
    calibration_focal_length_xy_pixel: tuple[float, float]
    calibration_principal_point_xy_pixel: tuple[float, float]
    calibration_distortion_coefficients: list[float]
    calibration_approximate_field_of_view_water_xy_degree: tuple[float, float]
    calibration_model_extra_description: str | None = None


class ImagePhotometricCalibration(BaseModel):
    """
    Represent photometric calibration parameters for image processing.

    This class encapsulates various photometric calibration settings used in image processing and analysis. It includes
    parameters for white balancing, exposure factors, illumination properties, and water characteristics. These
    attributes are crucial for accurate color representation and analysis in different lighting and environmental
    conditions.

    Attributes:
        photometric_sequence_white_balancing (str): The white balancing method used in the photometric sequence.
        photometric_exposure_factor_rgb (tuple[float, float, float]): RGB exposure factors for adjusting image exposure.
        photometric_sequence_illumination_type (str): The type of illumination used in the photometric sequence.
        photometric_sequence_illumination_description (str): A detailed description of the illumination setup.
        photometric_illumination_factor_rgb (tuple[float, float, float]): RGB illumination factors for color correction.
        photometric_water_properties_description (str): Description of water properties affecting light transmission.
    """

    photometric_sequence_white_balancing: str
    photometric_exposure_factor_rgb: tuple[float, float, float]
    photometric_sequence_illumination_type: str
    photometric_sequence_illumination_description: str
    photometric_illumination_factor_rgb: tuple[float, float, float]
    photometric_water_properties_description: str


class ImageCaptureFields(BaseModel):
    image_acquisition: ImageAcquisition | None = None
    image_quality: ImageQuality | None = None
    image_deployment: ImageDeployment | None = None
    image_navigation: ImageNavigation | None = None
    image_scale_reference: ImageScaleReference | None = None
    image_illumination: ImageIllumination | None = None
    image_pixel_magnitude: ImagePixelMagnitude | None = None
    image_marine_zone: ImageMarineZone | None = None
    image_spectral_resolution: ImageSpectralResolution | None = None
    image_capture_mode: ImageCaptureMode | None = None
    image_fauna_attraction: ImageFaunaAttraction | None = None
    image_area_square_meter: float | None = None
    image_meters_above_ground: float | None = None
    image_acquisition_settings: dict[str, Any] | None = None
    image_camera_yaw_degrees: float | None = None
    image_camera_pitch_degrees: float | None = None
    image_camera_roll_degrees: float | None = None
    image_overlap_fraction: float | None = None
    image_datetime_format: str | None = None
    image_camera_pose: ImageCameraPose | None = None
    image_camera_housing_viewport: ImageCameraHousingViewport | None = None
    image_flatport_parameters: ImageFlatportParameters | None = None
    image_domeport_parameters: ImageDomeportParameters | None = None
    image_camera_calibration_model: ImageCameraCalibrationModel | None = None
    image_photometric_calibration: ImagePhotometricCalibration | None = None
    image_objective: str | None = None
    image_target_environment: str | None = None
    image_target_timescale: str | None = None
    image_spatial_constraints: str | None = None
    image_temporal_constraints: str | None = None
    image_time_synchronization: str | None = None
    image_item_identification_scheme: str | None = None
    image_curation_protocol: str | None = None
