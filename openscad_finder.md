# anchorscad_lib.utils.openscad_finder

The `openscad_finder` module provides functionality to locate and determine the capabilities of the OpenSCAD executable on your system. It includes caching to avoid repeated system calls and supports multiple operating systems.

## Main Features

- Automatic OpenSCAD executable location
- Detection of available experimental features
- Detection of backend capabilities (e.g., Manifold support)
- Cross-platform support (Windows, macOS, Linux, BSD, Cygwin)
- Caching of OpenSCAD properties

## Basic Usage

```python
from anchorscad_lib.utils.openscad_finder import openscad_exe_properties

# Get OpenSCAD properties
properties = openscad_exe_properties()

# Print the executable path
print(properties.exe)

# Get recommended development options
dev_options = properties.dev_options()
```

## OpenscadProperties Class

The `OpenscadProperties` class contains information about the OpenSCAD executable:

```python
properties = openscad_exe_properties()

# Access the executable path
exe_path = properties.exe

# Check if manifold backend is available
manifold_opts = properties.manifold_option()

# Check if lazy union is available
lazy_union_opts = properties.lazy_union_option()

# Get all recommended development options
dev_opts = properties.dev_options()
```

### Available Properties

- `exe`: Path to the OpenSCAD executable
- `features`: Set of available experimental features
- `backend_has_manifold`: Boolean indicating if Manifold backend is available

## Search Locations

The module searches for OpenSCAD in the following order:

1. System PATH
2. Platform-specific standard locations:

### Windows
```
C:\Program Files\OpenSCAD (Nightly)\openscad.exe
D:\Program Files\OpenSCAD (Nightly)\openscad.exe
C:\Program Files\OpenSCADDev\openscad.exe
D:\Program Files\OpenSCADDev\openscad.exe
C:\Program Files\OpenSCAD\openscad.exe
D:\Program Files\OpenSCAD\openscad.exe
```

### macOS
```
/Applications/OpenSCAD.app/Contents/MacOS/openscad
```

### Linux/BSD
```
/usr/bin/openscad
/usr/local/bin/openscad
/usr/share/openscad/openscad
```

### Cygwin
```
/cygdrive/c/Program Files/OpenSCAD (Nightly)/openscad.exe
/cygdrive/d/Program Files/OpenSCAD (Nightly)/openscad.exe
/cygdrive/c/Program Files/OpenSCADDev/openscad.exe
/cygdrive/d/Program Files/OpenSCADDev/openscad.exe
/cygdrive/c/Program Files/OpenSCAD/openscad.exe
/cygdrive/d/Program Files/OpenSCAD/openscad.exe
```

## Caching

The module caches OpenSCAD properties in the user's home directory:

- Cache file: `~/.anchorscad_cache`
- Cache includes: executable path, modification time, size, features
- Cache is automatically invalidated when OpenSCAD is updated

## Command Line Usage

You can run the module directly to see OpenSCAD properties:

```bash
python -m anchorscad_lib.utils.openscad_finder
```

This will print the OpenSCAD properties and available development options.

## Installation

```bash
pip install anchorscad-utils
```

## Example Usage

### Basic Property Access
```python
from anchorscad_lib.utils.openscad_finder import openscad_exe_properties

properties = openscad_exe_properties()

print(f"OpenSCAD executable: {properties.exe}")

print(f"Available experimental features: {properties.features}")

print(f"Manifold backend is available: {properties.backend_has_manifold}")

print(f"Command line options that AnchorSCAD will use: {properties.dev_options()}")
```
