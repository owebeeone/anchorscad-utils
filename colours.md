# anchorscad_lib.colours

The `colours` module provides a colour handling system for AnchorSCAD, supporting RGB, RGBA, HSV, and named colours and colour transparency.

## Colour Class

The main class `Colour` provides functionality for creating and manipulating colours in various formats.

### Creating Colours

Colours can be created in several ways, see below for the constructor forms.

```python
    # Named Colors
    Colour('red')                    # Standard CSS color name
    Colour('red', 0.5)              # Named color with alpha

    # RGB/RGBA Values (0-1 range)
    Colour(1, 0, 0)                 # RGB as separate values
    Colour(1, 0, 0, 0.5)            # RGBA as separate values
    Colour((1, 0, 0))               # RGB as tuple
    Colour((1, 0, 0, 0.5))          # RGBA as tuple
    Colour(r=1, g=0, b=0)           # RGB as named parameters
    Colour(r=1, g=0, b=0, a=0.5)    # RGBA as named parameters

    # Hex Colors
    Colour('#FF0000')               # 6-digit hex
    Colour('#FF0000FF')             # 8-digit hex with alpha
    Colour('#F00')                  # 3-digit hex shorthand
    Colour('#F00F')                 # 4-digit hex shorthand with alpha

    # HSV Values (all components 0-1 range)
    Colour(hsv=(0, 1, 1))           # HSV as tuple
    Colour(hsv=(0, 1, 1, 0.5))      # HSVA as tuple

    # Copy Constructor
    Colour(some_other_colour)       # Create from existing Colour object
```

Note:
    - All numeric values are in the range 0-1
    - Alpha is optional and defaults to 1.0 (fully opaque)
    - HSV values must be provided as a tuple with the hsv= parameter
    - Hex colors support both 6/8-digit and 3/4-digit shorthand formats
    - Named colors are correspond to OpenSCAD's named colours.


### Colour Operations

The `Colour` class provides several methods for manipulating colours:

#### Alpha Modification

```python
colour = Colour('red')
semi_transparent = colour.alpha(0.5)
```

### Colour Operators

The `Colour` class supports several mathematical operators for color manipulation:

#### Addition (+)
```python
red = Colour('red')
blue = Colour('blue')
purple = red + blue  # Adds colors using Porter-Duff "over" compositing
```

#### Subtraction (-)
```python
white = Colour('white')
gray = Colour('gray')
light_gray = white - gray  # Subtracts colors while preserving alpha compositing
```

#### Multiplication (*)
```python
red = Colour('red')
darker = red * 0.5    # Scale RGB values by 0.5, keeping alpha unchanged
darker = 0.5 * red    # Same result (commutative)
```

#### Division (/)
```python
red = Colour('red')
lighter = red / 2.0   # Equivalent to red * 0.5
```

Note:
- Addition uses Porter-Duff "over" compositing for proper alpha handling
- Subtraction inverts the second color's RGB values before compositing
- Multiplication/division scales RGB values while preserving alpha
- Negative scaling factors invert the RGB values after scaling
- All operations clamp results to valid color ranges (0-1)


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
