# ifdo-py

ifdo-py is a Python library for the [iFDO](https://marine-imaging.com/fair/ifdos/iFDO-overview/) file format.

## Install

```bash
pip install ifdo
```

## Usage

### Read/write iFDO files
```python
from ifdo import iFDO

# Read from YAML file
ifdo_object = iFDO.load("path/to/ifdo.yaml")

# Write to YAML
ifdo_object.save("path/to/ifdo.yaml")
```

### Create image annotations
```python
from datetime import datetime
from ifdo.models import ImageAnnotation, AnnotationCoordinate, AnnotationLabel

# Create a bounding box
coordinates = [
    AnnotationCoordinate(x=0, y=0),
    AnnotationCoordinate(x=1, y=0),
    AnnotationCoordinate(x=1, y=1),
    AnnotationCoordinate(x=0, y=1),
]

# Create a label for it
label = AnnotationLabel(id="fish", annotator="kevin", created_at=datetime.now(), confidence=0.9)

# Pack it into an annotation
annotation = ImageAnnotation(coordinates=coordinates, labels=[label], shape='rectangle')

# Print it as a dictionary
print(annotation.to_dict())
```

```python
{
  'coordinates': [
    {'x': 0, 'y': 0}, 
    {'x': 1, 'y': 0}, 
    {'x': 1, 'y': 1}, 
    {'x': 0, 'y': 1}
  ], 
  'labels': [
    {
      'id': 'fish', 
      'annotator': 'kevin', 
      'created-at': datetime.datetime(2023, 2, 28, 16, 39, 46, 451290), 
      'confidence': 0.9
    }
  ], 
  'shape': 'rectangle'
}
```