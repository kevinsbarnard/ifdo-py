"""
Define and implement the Image FAIR Digital Object (iFDO) specification for image metadata management.

This module provides a comprehensive set of classes and data structures for representing, storing, and managing
metadata associated with image sets and individual images. It implements the iFDO specification, which aims to
make image data Findable, Accessible, Interoperable, and Reusable (FAIR). The module includes classes for
various aspects of image metadata, such as acquisition details, quality metrics, annotations, and calibration
information.

Imports:
    datetime: Provides classes for working with dates and times.
    enum: Supplies the Enum class for creating enumerated constants.
    pathlib: Offers classes representing filesystem paths with semantics appropriate for different operating systems.
    pydantic: Provides data validation and settings management using Python type annotations.
    stringcase: Offers string case conversion utilities.
    yaml: Implements YAML parser and emitter for Python.
    ifdo.model: Contains the base model implementation for iFDO classes.

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
    ImagePI: Represents an image Principal Investigator.
    ImageAnnotationLabel: Represents an image annotation label.
    ImageAnnotationCreator: Represents an image annotation creator.
    AnnotationLabel: Represents an annotation label with metadata.
    ImageAnnotation: Represents an image annotation with coordinates and labels.
    CameraPose: Represents a camera pose with UTM coordinates and orientation.
    CameraHousingViewport: Represents a camera housing viewport.
    FlatportParameters: Defines parameters for a flatport in an optical system.
    DomeportParameters: Defines parameters for a domeport in an optical system.
    CameraCalibrationModel: Defines a camera calibration model.
    PhotometricCalibration: Represents photometric calibration parameters.
    CoordinateValidation: Validates and stores image coordinate data.
    ImageData: Represents image data with associated metadata and annotations.
    ImageSetHeader: Represents an image set header with detailed metadata.
    iFDO: Implements the Image FAIR Digital Object specification.
"""

from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, field_validator
from stringcase import spinalcase
from yaml import safe_dump, safe_load

from ifdo.model import model

ifdo_model = model(case_func=spinalcase)  # Use spinal case for all field names


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


@ifdo_model
class ImagePI:
    """
    Represent an image PI (Principal Investigator) with associated information.

    This class models an image PI, typically used in scientific or research contexts where images are associated with
    a principal investigator. It stores the PI's name and ORCID (Open Researcher and Contributor ID) for proper
    attribution and identification.

    Attributes:
        name (str): The full name of the principal investigator.
        uri (str): A URI pointing to details of the PI. Could be an ORCID URI.
    """

    name: str
    uri: str | None = None


@ifdo_model
class ImageAnnotationLabel:
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


@ifdo_model
class ImageAnnotationCreator:
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


@ifdo_model
class AnnotationLabel:
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


@ifdo_model
class ImageAnnotation:
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


@ifdo_model
class CameraPose:
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


@ifdo_model
class CameraHousingViewport:
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


@ifdo_model
class FlatportParameters:
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


@ifdo_model
class DomeportParameters:
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


@ifdo_model
class CameraCalibrationModel:
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


@ifdo_model
class PhotometricCalibration:
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


@ifdo_model
class Context:
    """
    Represent a context within the ifdo model framework.

    This class defines a context, which is a common component in the ifdo model system. It encapsulates information
    about a named entity, optionally associated with a URI.

    Attributes:
        name (str): The name of the context.
        uri (str | None): An optional URI associated with the context. Defaults to None.
    """

    name: str
    uri: str | None = None

    def __hash__(self) -> int:
        return hash((self.name, self.uri))


@ifdo_model
class License:
    """
    Represent a software license.

    This class models a software license, typically used in software development and distribution. It stores
    the name of the license and optionally its URI (Uniform Resource Identifier).

    Attributes:
        name (str): The name of the license (e.g., "CC BY 4.0", "CC BY-NC 4.0", "CC BY-NC-ND 4.0").
        uri (str | None): The URI of the license text or details, if available. Defaults to None.
    """

    name: str
    uri: str | None = None

    def __hash__(self) -> int:
        return hash((self.name, self.uri))


class CoordinateValidation(BaseModel):
    """
    Validate and store image coordinate data.

    This class extends BaseModel to provide validation and storage for image coordinate data, specifically latitude
    and longitude. It ensures that the provided coordinates are within valid ranges and are not None. The class uses
    Pydantic's field validation system to enforce these constraints.

    Attributes:
        image_latitude (float | None): The latitude of the image, must be between -90 and 90 degrees.
        image_longitude (float | None): The longitude of the image, must be between -180 and 180 degrees.

    Methods:
        validate_latitude: Class method to validate the latitude value, ensuring it is not None.
        validate_longitude: Class method to validate the longitude value, ensuring it is not None.
    """

    image_latitude: float | None = Field(None, ge=-90, le=90)
    image_longitude: float | None = Field(None, ge=-180, le=180)

    @classmethod
    @field_validator("image_latitude")
    def validate_latitude(cls: type["CoordinateValidation"], value: float | None) -> float:
        """
        Validate the latitude value for image coordinates.

        This class method is a field validator for the 'image_latitude' field. It checks if the provided latitude value
        is not None, ensuring that a latitude is always provided for image coordinates. The method is used in
        conjunction with Pydantic's validation system.

        Args:
            cls (type['CoordinateValidation']): The class on which the validator is defined.
            value (float | None): The latitude value to be validated. Can be a float or None.

        Returns:
            float: The validated latitude value.

        Raises:
            ValueError: If the latitude value is None.
        """
        if value is None:
            raise ValueError("Latitude is required")
        return value

    @classmethod
    @field_validator("image_longitude")
    def validate_longitude(cls: type["CoordinateValidation"], value: float | None) -> float:
        """
        Validate the longitude value for image coordinates.

        This method is a class method and field validator for the 'image_longitude' field. It checks if the provided
        longitude value is not None and returns the value if valid. The method is designed to be used with Pydantic's
        field validation system.

        Args:
            cls (type['CoordinateValidation']): The class on which this method is called.
            value (float | None): The longitude value to be validated, can be a float or None.

        Returns:
            float: The validated longitude value.

        Raises:
            ValueError: If the longitude value is None.
        """
        if value is None:
            raise ValueError("Longitude is required")
        return value


@ifdo_model
class ImageData:
    """
    Represent image data with associated metadata and annotations.

    This class encapsulates comprehensive information about an image, including its metadata, acquisition details,
    quality metrics, annotations, and various other properties. It is designed to store and manage a wide range of
    attributes related to image capture, processing, and analysis.

    Attributes:
        image_datetime (datetime | None): Date and time when the image was captured.
        image_latitude (float | None): Latitude coordinate of the image location, range: -90 to 90.
        image_longitude (float | None): Longitude coordinate of the image location, range: -180 to 180.
        image_altitude_meters (float | None): Altitude at which the image was captured.
        image_coordinate_reference_system (str | None): Coordinate reference system used for geolocation.
        image_coordinate_uncertainty_meters (float | None): Uncertainty of the coordinate measurement in meters.
        image_context (Context | None): Context or setting in which the image was captured.
        image_project (Context | None): Project or study associated with the image.
        image_event (Context | None): Specific event during which the image was captured.
        image_platform (Context | None): Platform or vehicle used for image capture.
        image_sensor (Context | None): Sensor or camera used to capture the image.
        image_uuid (str | None): Unique identifier for the image.
        image_hash_sha256 (str | None): SHA256 hash of the image file.
        image_pi (ImagePI | None): Principal investigator information.
        image_creators (list[ImagePI] | None): List of individuals who created or contributed to the image.
        image_license (License | None): License information for the image.
        image_copyright (str | None): Copyright information for the image.
        image_abstract (str | None): Brief description or abstract of the image content.
        image_acquisition (ImageAcquisition | None): Details about the image acquisition process.
        image_quality (ImageQuality | None): Quality metrics for the image.
        image_deployment (ImageDeployment | None): Information about the deployment of the imaging equipment.
        image_navigation (ImageNavigation | None): Navigation data associated with the image capture.
        image_scale_reference (ImageScaleReference | None): Scale reference information for the image.
        image_illumination (ImageIllumination | None): Illumination conditions during image capture.
        image_pixel_magnitude (ImagePixelMagnitude | None): Pixel magnitude information.
        image_marine_zone (ImageMarineZone | None): Marine zone classification for the image location.
        image_spectral_resolution (ImageSpectralResolution | None): Spectral resolution of the image.
        image_capture_mode (ImageCaptureMode | None): Mode of image capture (e.g., continuous, triggered).
        image_fauna_attraction (ImageFaunaAttraction | None): Information about fauna attraction methods used.
        image_area_square_meter (float | None): Area covered by the image in square meters.
        image_meters_above_ground (float | None): Height of the camera above the ground or sea floor.
        image_acquisition_settings (dict[str, Any] | None): Camera settings used during image acquisition.
        image_camera_yaw_degrees (float | None): Camera yaw angle in degrees.
        image_camera_pitch_degrees (float | None): Camera pitch angle in degrees.
        image_camera_roll_degrees (float | None): Camera roll angle in degrees.
        image_overlap_fraction (float | None): The average overlap of two consecutive images.
        image_datetime_format (str | None): Format used for the image_datetime field.
        image_camera_pose (CameraPose | None): Camera pose information.
        image_camera_housing_viewport (CameraHousingViewport | None): Information about the camera housing viewport.
        image_flatport_parameters (FlatportParameters | None): Parameters for flat port camera housings.
        image_domeport_parameters (DomeportParameters | None): Parameters for dome port camera housings.
        image_camera_calibration_model (CameraCalibrationModel | None): Camera calibration model information.
        image_photometric_calibration (PhotometricCalibration | None): Photometric calibration information.
        image_objective (str | None): Objective or purpose of the image capture.
        image_target_environment (str | None): Target environment for the image capture.
        image_target_timescale (str | None): Target timescale for the image capture.
        image_spatial_constraints (str | None): Spatial constraints for the image capture.
        image_temporal_constraints (str | None): Temporal constraints for the image capture.
        image_time_synchronization (str | None): Method used for time synchronization.
        image_item_identification_scheme (str | None): Scheme used for identifying items in the image.
        image_curation_protocol (str | None): Protocol used for image curation.
        image_entropy (float | None): Entropy value of the image.
        image_particle_count (int | None): Count of particles detected in the image.
        image_average_color (list[int] | None): Average color of the image as RGB values.
        image_mpeg7_colorlayout (list[float] | None): MPEG-7 color layout descriptor.
        image_mpeg7_colorstatistics (list[float] | None): MPEG-7 color statistics descriptor.
        image_mpeg7_colorstructure (list[float] | None): MPEG-7 color structure descriptor.
        image_mpeg7_dominantcolor (list[float] | None): MPEG-7 dominant color descriptor.
        image_mpeg7_edgehistogram (list[float] | None): MPEG-7 edge histogram descriptor.
        image_mpeg7_homogenoustexture (list[float] | None): MPEG-7 homogeneous texture descriptor.
        image_mpeg7_stablecolor (list[float] | None): MPEG-7 stable color descriptor.
        image_annotation_labels (list[ImageAnnotationLabel] | None): List of annotation labels for the image.
        image_annotation_creators (list[ImageAnnotationCreator] | None): List of annotation creators.
        image_annotations (list[ImageAnnotation] | None): List of annotations for the image.
    """

    # iFDO core
    image_datetime: datetime | None = None
    image_latitude: float | None = Field(None, ge=-90, le=90)
    image_longitude: float | None = Field(None, ge=-180, le=180)
    image_altitude_meters: float | None = None
    image_coordinate_reference_system: str | None = None
    image_coordinate_uncertainty_meters: float | None = None
    image_context: Context | None = None
    image_project: Context | None = None
    image_event: Context | None = None
    image_platform: Context | None = None
    image_sensor: Context | None = None
    image_uuid: str | None = None
    image_hash_sha256: str | None = None
    image_pi: ImagePI | None = None
    image_creators: list[ImagePI] | None = None
    image_license: License | None = None
    image_copyright: str | None = None
    image_abstract: str | None = None

    # iFDO capture (optional)
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
    image_camera_pose: CameraPose | None = None
    image_camera_housing_viewport: CameraHousingViewport | None = None
    image_flatport_parameters: FlatportParameters | None = None
    image_domeport_parameters: DomeportParameters | None = None
    image_camera_calibration_model: CameraCalibrationModel | None = None
    image_photometric_calibration: PhotometricCalibration | None = None
    image_objective: str | None = None
    image_target_environment: str | None = None
    image_target_timescale: str | None = None
    image_spatial_constraints: str | None = None
    image_temporal_constraints: str | None = None
    image_time_synchronization: str | None = None
    image_item_identification_scheme: str | None = None
    image_curation_protocol: str | None = None

    # iFDO content (optional)
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


@ifdo_model
class ImageSetHeader:
    """
    Represent an image set header with detailed metadata and attributes.

    This class encapsulates comprehensive information about an image set, including identification, geospatial data,
    acquisition details, quality metrics, and various parameters related to image capture and processing. It is designed
    to provide a standardized structure for storing and managing image set metadata in scientific and research contexts.

    Attributes:
        image_datetime (datetime | None): Date and time when the image was captured.
        image_latitude (float | None): Latitude coordinate of the image location, range: -90 to 90.
        image_longitude (float | None): Longitude coordinate of the image location, range: -180 to 180.
        image_altitude_meters (float | None): Altitude at which the image was captured.
        image_coordinate_reference_system (str | None): Coordinate reference system used for geolocation.
        image_coordinate_uncertainty_meters (float | None): Uncertainty of the coordinate measurement in meters.
        image_context (Context | None): Context or setting in which the image was captured.
        image_project (Context | None): Project or study associated with the image.
        image_event (Context | None): Specific event during which the image was captured.
        image_platform (Context | None): Platform or vehicle used for image capture.
        image_sensor (Context | None): Sensor or camera used to capture the image.
        image_uuid (str | None): Unique identifier for the image.
        image_hash_sha256 (str | None): SHA256 hash of the image file.
        image_pi (ImagePI | None): Principal investigator information.
        image_creators (list[ImagePI] | None): List of individuals who created or contributed to the image.
        image_license (License | None): License information for the image.
        image_copyright (str | None): Copyright information for the image.
        image_abstract (str | None): Brief description or abstract of the image content.
        image_acquisition (ImageAcquisition | None): Details about the image acquisition process.
        image_quality (ImageQuality | None): Quality metrics for the image.
        image_deployment (ImageDeployment | None): Information about the deployment of the imaging equipment.
        image_navigation (ImageNavigation | None): Navigation data associated with the image capture.
        image_scale_reference (ImageScaleReference | None): Scale reference information for the image.
        image_illumination (ImageIllumination | None): Illumination conditions during image capture.
        image_pixel_magnitude (ImagePixelMagnitude | None): Pixel magnitude information.
        image_marine_zone (ImageMarineZone | None): Marine zone classification for the image location.
        image_spectral_resolution (ImageSpectralResolution | None): Spectral resolution of the image.
        image_capture_mode (ImageCaptureMode | None): Mode of image capture (e.g., continuous, triggered).
        image_fauna_attraction (ImageFaunaAttraction | None): Information about fauna attraction methods used.
        image_area_square_meter (float | None): Area covered by the image in square meters.
        image_meters_above_ground (float | None): Height of the camera above the ground or sea floor.
        image_acquisition_settings (dict[str, Any] | None): Camera settings used during image acquisition.
        image_camera_yaw_degrees (float | None): Camera yaw angle in degrees.
        image_camera_pitch_degrees (float | None): Camera pitch angle in degrees.
        image_camera_roll_degrees (float | None): Camera roll angle in degrees.
        image_overlap_fraction (float | None): The average overlap of two consecutive images.
        image_datetime_format (str | None): Format used for the image_datetime field.
        image_camera_pose (CameraPose | None): Camera pose information.
        image_camera_housing_viewport (CameraHousingViewport | None): Information about the camera housing viewport.
        image_flatport_parameters (FlatportParameters | None): Parameters for flat port camera housings.
        image_domeport_parameters (DomeportParameters | None): Parameters for dome port camera housings.
        image_camera_calibration_model (CameraCalibrationModel | None): Camera calibration model information.
        image_photometric_calibration (PhotometricCalibration | None): Photometric calibration information.
        image_objective (str | None): Objective or purpose of the image capture.
        image_target_environment (str | None): Target environment for the image capture.
        image_target_timescale (str | None): Target timescale for the image capture.
        image_spatial_constraints (str | None): Spatial constraints for the image capture.
        image_temporal_constraints (str | None): Temporal constraints for the image capture.
        image_time_synchronization (str | None): Method used for time synchronization.
        image_item_identification_scheme (str | None): Scheme used for identifying items in the image.
        image_curation_protocol (str | None): Protocol used for image curation.
        image_entropy (float | None): Entropy value of the image.
        image_particle_count (int | None): Count of particles detected in the image.
        image_average_color (list[int] | None): Average color of the image as RGB values.
        image_mpeg7_colorlayout (list[float] | None): MPEG-7 color layout descriptor.
        image_mpeg7_colorstatistics (list[float] | None): MPEG-7 color statistics descriptor.
        image_mpeg7_colorstructure (list[float] | None): MPEG-7 color structure descriptor.
        image_mpeg7_dominantcolor (list[float] | None): MPEG-7 dominant color descriptor.
        image_mpeg7_edgehistogram (list[float] | None): MPEG-7 edge histogram descriptor.
        image_mpeg7_homogenoustexture (list[float] | None): MPEG-7 homogeneous texture descriptor.
        image_mpeg7_stablecolor (list[float] | None): MPEG-7 stable color descriptor.
        image_annotation_labels (list[ImageAnnotationLabel] | None): List of annotation labels for the image.
        image_annotation_creators (list[ImageAnnotationCreator] | None): List of annotation creators.
        image_annotations (list[ImageAnnotation] | None): List of annotations for the image.
    """

    image_set_name: str
    image_set_uuid: str
    image_set_handle: str
    image_set_ifdo_version: str = "v2.1.0"

    # iFDO core
    image_datetime: datetime | None = None
    image_latitude: float | None = Field(None, ge=-90, le=90)
    image_longitude: float | None = Field(None, ge=-180, le=180)
    image_altitude_meters: float | None = None
    image_coordinate_reference_system: str | None = None
    image_coordinate_uncertainty_meters: float | None = None
    image_context: Context | None = None
    image_project: Context | None = None
    image_event: Context | None = None
    image_platform: Context | None = None
    image_sensor: Context | None = None
    image_uuid: str | None = None
    image_hash_sha256: str | None = None
    image_pi: ImagePI | None = None
    image_creators: list[ImagePI] | None = None
    image_license: License | None = None
    image_copyright: str | None = None
    image_abstract: str | None = None

    # iFDO capture (optional)
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
    image_camera_pose: CameraPose | None = None
    image_camera_housing_viewport: CameraHousingViewport | None = None
    image_flatport_parameters: FlatportParameters | None = None
    image_domeport_parameters: DomeportParameters | None = None
    image_camera_calibration_model: CameraCalibrationModel | None = None
    image_photometric_calibration: PhotometricCalibration | None = None
    image_objective: str | None = None
    image_target_environment: str | None = None
    image_target_timescale: str | None = None
    image_spatial_constraints: str | None = None
    image_temporal_constraints: str | None = None
    image_time_synchronization: str | None = None
    image_item_identification_scheme: str | None = None
    image_curation_protocol: str | None = None

    # iFDO content (optional)
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


@ifdo_model
class iFDO:  # noqa: N801
    """
    Class implementation of the Image FAIR Digital Object (iFDO) specification.

    This class encapsulates the structure and functionality of an iFDO, which includes a header containing metadata
    about the image set and a dictionary of image data items. It provides methods for loading from and saving to YAML
    files, making it easy to persist and retrieve iFDO objects.

    Attributes:
        image_set_header (ImageSetHeader): Contains metadata information about the image set.
        image_set_items (dict[str, list[ImageData]]): A dictionary mapping keys to lists of ImageData objects.

    Methods:
        load(path: str | Path) -> 'iFDO': Class method to load an iFDO object from a YAML file.
        save(path: str | Path) -> None: Instance method to save the iFDO object to a YAML file.

    Example:
        # Load an existing iFDO from a YAML file
        ifdo = iFDO.load('path/to/ifdo.yaml')

        # Access and modify attributes
        print(ifdo.image_set_header)
        ifdo.image_set_items['key'] = [ImageData(...), ImageData(...)]

        # Save the modified iFDO to a new YAML file
        ifdo.save('path/to/new_ifdo.yaml')
    """

    image_set_header: ImageSetHeader
    image_set_items: dict[str, list[ImageData]]

    @classmethod
    def load(cls, path: str | Path) -> "iFDO":
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

    def save(self, path: str | Path) -> None:
        """
        Save to a YAML file.

        Args:
            path: Path to the YAML file.
        """
        path = Path(path)  # Ensure Path object
        with path.open("w") as f:
            safe_dump(self.to_dict(), f, sort_keys=False)
