from typing import Optional, Callable, Union, get_args, get_origin
from dataclasses import dataclass, fields, MISSING


def serializable(case_func: Optional[Callable] = None):
    """
    Decorator that creates a dataclass with methods to convert it to/from a dict object.

    Args:
        case_func: Optional function to transform field names (e.g. stringcase.spinalcase). Default is None.

    Returns:
        Decorator function that converts a class into a dataclass with to_dict and from_dict methods.
    """
    def decorator(cls):
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
                if isinstance(value, list):
                    d[name] = [item.to_dict() if hasattr(item, 'to_dict') else item for item in value]
                elif isinstance(value, dict):
                    d[name] = {k: v.to_dict() if hasattr(v, 'to_dict') else v for k, v in value.items()}
                elif hasattr(value, 'to_dict'):
                    d[name] = value.to_dict()
                else:
                    d[name] = value
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
                field_name = field.name
                field_type = field.type
                field_origin = get_origin(field_type)
                field_args = get_args(field_type)
                
                optional = field_origin is Union and type(None) in field_args  # Check if Optional
                if optional and len(field_args) > 2:  # Reject Union with NoneType with more than 2 types
                    raise ValueError(f'Union with NoneType with more than 2 types is not supported: {field_name}')
                
                if case_func is not None:  # Remap by case function
                    field_name = case_func(field_name)
                
                if field_name in d:
                    value = d[field_name]
                    
                    if optional:  # if Optional, set the type to be the non-None type
                        field_type = field_args[0]
                        field_origin = get_origin(field_type)
                        field_args = get_args(field_type)
                    
                    if field_origin is list and isinstance(value, list):
                        inner_type = field_args[0]
                        inner_values = [inner_type.from_dict(v) if hasattr(inner_type, 'from_dict') else v for v in value]
                        kwargs[field.name] = inner_values
                    elif field_origin is dict and isinstance(value, dict):
                        inner_types = field_args
                        inner_key_type, inner_value_type = inner_types[0], inner_types[1]
                        inner_values = {
                            inner_key_type(vk): (
                                inner_value_type.from_dict(vv) 
                                if hasattr(inner_value_type, 'from_dict') else vv
                            ) 
                            for vk, vv in value.items()
                        }
                        kwargs[field.name] = inner_values
                    else:
                        if hasattr(field_type, 'from_dict'):
                            kwargs[field.name] = field_type.from_dict(value)
                        elif isinstance(value, field_type) or value is None:
                            kwargs[field.name] = value
                        else:
                            kwargs[field.name] = field_type(value)
                elif field.default != MISSING:
                    kwargs[field.name] = field.default
                elif field.default_factory != MISSING:
                    kwargs[field.name] = field.default_factory()
                elif not optional:
                    raise ValueError(f"Missing required field '{field_name}' in dict {d}")
            return cls(**kwargs)

        # Add the new methods to the class
        cls.to_dict = to_dict
        cls.from_dict = classmethod(from_dict)

        # Return the modified class
        return cls
    return decorator
