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
    ImageData: Represents image data with associated metadata and annotations.
    ImageSetHeader: Represents an image set header with detailed metadata.
    iFDO: Implements the Image FAIR Digital Object specification.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict
from stringcase import spinalcase

from ifdo.models.ifdo_capture import ImageCaptureFields
from ifdo.models.ifdo_content import ImageContentFields
from ifdo.models.ifdo_core import ImageCoreFields


class KebabCaseModel(BaseModel):
    model_config = ConfigDict(alias_generator=spinalcase, populate_by_name=True)


class ImageData(KebabCaseModel, ImageCoreFields, ImageCaptureFields, ImageContentFields):
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
        image_context (ImageContext | None): Context or setting in which the image was captured.
        image_project (ImageContext | None): Project or study associated with the image.
        image_event (ImageContext | None): Specific event during which the image was captured.
        image_platform (ImageContext | None): Platform or vehicle used for image capture.
        image_sensor (ImageContext | None): Sensor or camera used to capture the image.
        image_uuid (str | None): Unique identifier for the image.
        image_hash_sha256 (str | None): SHA256 hash of the image file.
        image_handle (str | None): Handle pointing to image.
        image_pi (ImagePI | None): Principal investigator information.
        image_creators (list[ImageCreator] | None): List of individuals who created or contributed to the image.
        image_license (ImageLicense | None): License information for the image.
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
        image_camera_pose (ImageCameraPose | None): Camera pose information.
        image_camera_housing_viewport (ImageCameraHousingViewport | None): Information about the camera housing viewport.
        image_flatport_parameters (ImageFlatportParameters | None): Parameters for flat port camera housings.
        image_domeport_parameters (ImageDomeportParameters | None): Parameters for dome port camera housings.
        image_camera_calibration_model (ImageCameraCalibrationModel | None): Camera calibration model information.
        image_photometric_calibration (ImagePhotometricCalibration | None): Photometric calibration information.
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

    image_uuid: str | None = None
    image_hash_sha256: str | None = None
    image_handle: str | None = None


class ImageSetHeader(KebabCaseModel, ImageCoreFields, ImageCaptureFields, ImageContentFields):
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
        image_context (ImageContext | None): Context or setting in which the image was captured.
        image_project (ImageContext | None): Project or study associated with the image.
        image_event (ImageContext | None): Specific event during which the image was captured.
        image_platform (ImageContext | None): Platform or vehicle used for image capture.
        image_sensor (ImageContext | None): Sensor or camera used to capture the image.
        image_pi (ImagePI | None): Principal investigator information.
        image_creators (list[ImageCreator] | None): List of individuals who created or contributed to the image.
        image_license (ImageLicense | None): License information for the image.
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
        image_camera_pose (ImageCameraPose | None): Camera pose information.
        image_camera_housing_viewport (ImageCameraHousingViewport | None): Information about the camera housing viewport.
        image_flatport_parameters (ImageFlatportParameters | None): Parameters for flat port camera housings.
        image_domeport_parameters (ImageDomeportParameters | None): Parameters for dome port camera housings.
        image_camera_calibration_model (ImageCameraCalibrationModel | None): Camera calibration model information.
        image_photometric_calibration (ImagePhotometricCalibration | None): Photometric calibration information.
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
        image_uuid (str | None): Unique identifier for the image. Should not be set in the header.
        image_hash_sha256 (str | None): SHA256 hash of the image file. Should not be set in the header.
        image_handle (str | None): Handle pointing to image. Should not be set in the header.
    """

    image_set_name: str
    image_set_uuid: str
    image_set_handle: str
    image_set_ifdo_version: str = "v2.1.0"

    image_uuid: str | None = None
    image_hash_sha256: str | None = None
    image_handle: str | None = None


class iFDO(KebabCaseModel):  # noqa: N801
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
    def from_dict(cls, data: dict[str, Any]) -> iFDO:
        return cls.model_validate(data)

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json", by_alias=True, exclude_none=True)

    @classmethod
    def load(cls, path: str | Path) -> "iFDO":
        """
        Load an iFDO from a YAML or JSON file.

        Args:
            path: Path to the file. Should have a suffix of `.yaml`, `.yml`, or `.json`.

        Returns:
            The loaded iFDO object.

        Raises:
            ValueError: If the file format is not supported.
        """
        path = Path(path)  # Ensure Path object
        with path.open() as f:
            suffix = path.suffix.lower().lstrip(".")
            if suffix in ("yaml", "yml"):
                d = yaml.safe_load(f)
            elif suffix == "json":
                d = json.load(f)
            else:
                raise ValueError("Unsupported file format. Use YAML (.yaml, .yml) or JSON (.json).")

        return cls.from_dict(d)

    def save(self, path: str | Path) -> None:
        """
        Save to a YAML or JSON file. Should have a suffix of `.yaml`, `.yml`, or `.json`.

        Args:
            path: Path to the file.

        Raises:
            ValueError: If the file format is not supported
        """
        path = Path(path)  # Ensure Path object
        with path.open("w") as f:
            suffix = path.suffix.lower().lstrip(".")
            if suffix in ("yaml", "yml"):
                yaml.safe_dump(self.to_dict(), f, sort_keys=False)
            elif suffix == "json":
                json.dump(self.to_dict(), f, indent=2)
            else:
                raise ValueError(
                    "Unsupported file format. Use YAML (.yaml, .yml) or JSON (.json).",
                )
