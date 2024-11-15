from collections.abc import Callable
from dataclasses import MISSING, fields
from datetime import datetime
from enum import Enum
from typing import Any, TypeVar, Union, get_args, get_origin

from pydantic.dataclasses import dataclass


def parse_value(field_class, value: Any) -> Any:
    """
    Parse a value given its class.

    Args:
        field_class: Class of the value
        value: Value to parse

    Returns:
        Parsed value
    """
    if hasattr(field_class, "from_dict"):
        return field_class.from_dict(value)
    if issubclass(field_class, Enum):
        return field_class(value)
    if issubclass(field_class, datetime):
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")
    return value


def parse_field(field_type, value: Any) -> Any:
    """
    Parse a field value given its type annotation.

    Args:
        field_type: Type annotation of the field
        value: Value to parse

    Returns:
        Parsed value
    """
    field_origin = get_origin(field_type)
    field_args = get_args(field_type)

    optional = field_origin is Union and type(None) in field_args  # Check if Optional
    if optional and len(field_args) > 2:  # Reject Union with NoneType with more than 2 types
        raise ValueError(f"Union with NoneType with more than 2 types is not supported: {field_type}")

    if optional:  # If Optional, set the type to be the non-None type
        field_type = field_args[0]
        field_origin = get_origin(field_type)
        field_args = get_args(field_type)
    elif value is None:  # If not Optional, raise an error if the value is None before we try to parse it
        raise ValueError(f"Value is None but field type '{field_type}' is not Optional")

    if field_origin is list:
        inner_type = field_args[0]
        return [parse_field(inner_type, v) for v in value]
    if field_origin is tuple:
        return tuple(parse_field(inner_type, v) for inner_type, v in zip(field_args, value, strict=False))
    if field_origin is dict:
        inner_key_type, inner_value_type = field_args
        return {parse_field(inner_key_type, k): parse_field(inner_value_type, v) for k, v in value.items()}
    if field_origin is Union:
        for inner_type in field_args:
            try:
                return parse_field(inner_type, value)
            except ValueError:
                pass
        raise ValueError(f"Could not parse value {value} as any of {field_args}")
    return parse_value(field_type, value)


def encode_value(value: Any) -> Any:
    """
    Encode a value to be JSON serializable.

    Args:
        value: Value to encode

    Returns:
        Encoded value
    """
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, datetime):
        return datetime.strftime(value, "%Y-%m-%d %H:%M:%S.%f")
    if isinstance(value, list):
        return [encode_value(v) for v in value]
    if isinstance(value, tuple):
        return tuple(encode_value(v) for v in value)
    if isinstance(value, dict):
        return {encode_value(k): encode_value(v) for k, v in value.items()}
    if hasattr(value, "to_dict"):
        return value.to_dict()
    return value


T = TypeVar("T")


def model(case_func: Callable | None = None) -> Callable[[type[T]], type[T]]:
    """
    Decorator that creates a dataclass with methods to convert it to/from a dict object.

    Args:
        case_func: Optional function to transform field names (e.g. stringcase.spinalcase). Default is None.

    Returns:
        Decorator function that converts a class into a dataclass with to_dict and from_dict methods.
    """

    def decorator(cls: type[T]) -> type[T]:
        # Turn the class into a dataclass
        cls = dataclass(cls)

        # Define the to_dict method
        def to_dict(self) -> dict:
            """
            Convert the object to a dict object.

            Returns:
                dict object
            """
            d = dict()
            for field in fields(self):
                name = field.name
                if case_func is not None:
                    name = case_func(name)
                value = getattr(self, field.name)
                if value is None:
                    continue

                encoded_value = encode_value(value)

                d[name] = encoded_value
            return d

        # Define the from_dict method
        def from_dict(cls, d: dict):
            """
            Convert a dict object to an object of this class.

            Args:
                d: dict object

            Returns:
                Object of this class
            """
            kwargs = {}
            for field in fields(cls):
                field_key = field.name
                if case_func is not None:  # Remap by case function
                    field_key = case_func(field_key)

                if field_key in d:
                    value = d[field_key]

                    try:
                        parsed_value = parse_field(field.type, value)
                    except ValueError as e:
                        raise ValueError(f"Could not parse value {value} for field {field_key}: {e}")

                    if parsed_value is None:  # Use default value/factory if parsed value is None
                        if field.default != MISSING:
                            parsed_value = field.default
                        elif field.default_factory != MISSING:
                            parsed_value = field.default_factory()

                    # Assign the parsed value to the kwargs
                    kwargs[field.name] = parsed_value

            # Create the object from the kwargs
            return cls(**kwargs)

        # Add the new methods to the class
        cls.to_dict = to_dict
        cls.from_dict = classmethod(from_dict)

        # Return the modified class
        return cls

    return decorator
