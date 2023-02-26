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

# Read from YAML
ifdo = iFDO.from_yaml("path/to/ifdo.yaml")

# Write to YAML
ifdo.to_yaml("path/to/ifdo.yaml")

# Write to JSON
ifdo.to_json("path/to/ifdo.json")
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

# Print it as a YAML string
print(annotation.to_yaml())
```

```yaml
coordinates:
- x: 0
  y: 0
- x: 1
  y: 0
- x: 1
  y: 1
- x: 0
  y: 1
labels:
- annotator: kevin
  confidence: 0.9
  created-at: '2023-02-26T14:19:54.604209'
  id: fish
shape: rectangle
```