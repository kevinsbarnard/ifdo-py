from datetime import datetime
from enum import Enum
from typing import Any, Optional, Callable, Union, TypeVar, Type, get_args, get_origin
from dataclasses import dataclass, fields, MISSING


def parse_value(field_class, value: Any, coerce: bool = False) -> Any:
    """
    Parse a value given its class.
    
    Args:
        field_class: Class of the value
        value: Value to parse
        coerce: Whether to coerce the value to the field class. Default is False.
    
    Returns:
        Parsed value
    """
    if hasattr(field_class, 'from_dict'):
        return field_class.from_dict(value, coerce=coerce)
    elif issubclass(field_class, Enum):
        return field_class(value)
    elif coerce:
        return value if isinstance(value, field_class) else field_class(value)
    else:
        return value


def parse_field(field_type, value: Any, coerce: bool = False) -> Any:
    """
    Parse a field value given its type annotation.
    
    Args:
        field_type: Type annotation of the field
        value: Value to parse
        coerce: Whether to coerce the value to the field class. Default is False.
    
    Returns:
        Parsed value
    """
    field_origin = get_origin(field_type)
    field_args = get_args(field_type)
    
    optional = field_origin is Union and type(None) in field_args  # Check if Optional
    if optional and len(field_args) > 2:  # Reject Union with NoneType with more than 2 types
        raise ValueError(f'Union with NoneType with more than 2 types is not supported: {field_type}')
    
    if optional:  # If Optional, set the type to be the non-None type
        field_type = field_args[0]
        field_origin = get_origin(field_type)
        field_args = get_args(field_type)
    elif value is None:  # If not Optional, raise an error if the value is None before we try to parse it
        raise ValueError(f"Value is None but field type '{field_type}' is not Optional")
    
    if field_origin is list:
        inner_type = field_args[0]
        return [parse_field(inner_type, v, coerce=coerce) for v in value]
    elif field_origin is tuple:
        return tuple(parse_field(inner_type, v, coerce=coerce) for inner_type, v in zip(field_args, value))
    elif field_origin is dict:
        inner_key_type, inner_value_type = field_args
        return {parse_field(inner_key_type, k, coerce=coerce): parse_field(inner_value_type, v, coerce=coerce) for k, v in value.items()}
    elif field_origin is Union:
        for inner_type in field_args:
            try:
                return parse_field(inner_type, value, coerce=coerce)
            except ValueError:
                pass
        raise ValueError(f'Could not parse value {value} as any of {field_args}')
    else:
        return parse_value(field_type, value, coerce=coerce)


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
    elif isinstance(value, datetime):
        return value.isoformat()
    elif isinstance(value, list):
        return [encode_value(v) for v in value]
    elif isinstance(value, tuple):
        return tuple(encode_value(v) for v in value)
    elif isinstance(value, dict):
        return {encode_value(k): encode_value(v) for k, v in value.items()}
    elif hasattr(value, 'to_dict'):
        return value.to_dict()
    else:
        return value


T = TypeVar("T")
def model(case_func: Optional[Callable] = None) -> Callable[[Type[T]], Type[T]]:
    """
    Decorator that creates a dataclass with methods to convert it to/from a dict object.

    Args:
        case_func: Optional function to transform field names (e.g. stringcase.spinalcase). Default is None.

    Returns:
        Decorator function that converts a class into a dataclass with to_dict and from_dict methods.
    """
    def decorator(cls: Type[T]) -> Type[T]:
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
        def from_dict(cls, d: dict, coerce: bool = False):
            """
            Convert a dict object to an object of this class.
            
            Args:
                d: dict object
                coerce: If True, coerce values to the annotated types.
            
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
                        parsed_value = parse_field(field.type, value, coerce=coerce)
                    except ValueError as e:
                        raise ValueError(f'Could not parse value {value} for field {field_key}: {e}')
                    
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
