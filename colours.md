# anchorscad_lib.colours

The `colours` module provides a colour handling system for AnchorSCAD, supporting RGB, RGBA, HSV, and named colours and colour transparency.

## Colour Class

The main class `Colour` provides functionality for creating and manipulating colours in various formats.

### Creating Colours

Colours can be created in several ways:

1. Using named colours:

```pythonpython
red = Colour('red')
blue = Colour('blue')
transparent = Colour('transparent')
```

2. Using RGB values:

```python
red = Colour(1, 0, 0)
green = Colour(0, 1, 0)
blue = Colour(0, 0, 1)
```
3. Using RGBA values:

```python
semi_transparent_red = Colour(1, 0, 0, 0.5)
or
semi_transparent_red = Colour((1, 0, 0, 0.5))
```

4. Using hex colour strings:

```python
red = Colour(hsv=(0, 1, 1))
semi_transparent_red = Colour(hsv=(0, 1, 1, 0.5))
```

5. Using HSV values:

```python
red = Colour(hsv=(0, 1, 1))
semi_transparent_red = Colour(hsv=(0, 1, 1, 0.5))
```


### Colour Operations

The `Colour` class provides several methods for manipulating colours:

#### Alpha Modification

```python
colour = Colour('red')
semi_transparent = colour.alpha(0.5)
```

#### Colour Blending

```python
red = Colour('red')
blue = Colour('blue')
purple = red.blend(blue, 0.5) # Blend red and blue equally
```

### Colour Conversions

Colours can be converted between different formats:

```python   
colour = Colour('red')
hex_string = colour.to_hex() # Convert to hex string
hsv_tuple = colour.to_hsv() # Convert to HSV tuple
```

### Colour Properties

The `Colour` class provides several properties for accessing colour information:

```python
colour = Colour('red')
print(colour.r) # Access red component
print(colour.g) # Access green component
print(colour.b) # Access blue component
print(colour.a) # Access alpha component
```

### Supported Colour Names

The module includes a comprehensive list of named colours matching the CSS colour names. Some examples include:

- Basic colours: 'red', 'green', 'blue', 'yellow', etc.
- Extended colours: 'coral', 'crimson', 'darkblue', etc.
- Special colours: 'transparent'

For a complete list of supported colour names, refer to the `COLOUR_MAP` dictionary in the source code. This list was lifted from OpenSCAD's [`ColorNode.cc` file](https://github.com/openscad/openscad/blob/master/src/core/ColorNode.cc#L46).

### Technical Details

- All colour values are stored internally as RGBA tuples with values between 0 and 1
- The class is immutable (frozen=True) to prevent accidental modifications
- All colour operations return new Colour instances
- HSV values are automatically converted to RGB for internal storage

### Usage in to_3mf

The Colour class was extracted from AnchorSCAD's core library because it is used by the `to_3mf` module and it's generally a useful colour abstraction.

## Installation

```bash
pip install anchorscad-utils
```

## Usage

```python
from anchorscad_utils.colours import Colour

red = Colour('red')
print(red.to_hex())
```


