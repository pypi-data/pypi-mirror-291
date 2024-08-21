# Real

**Real** is a Python class designed to calculate the real screen size, including the width, height, and area, based on the diagonal measurement and aspect ratio of the screen. This can be especially useful for calculating the dimensions of TVs, monitors, or other displays.

## Features

- **Calculate Screen Dimensions**: Determine the width, height, and area of a screen given its diagonal size and aspect ratio.
- **Support for Custom Aspect Ratios**: Easily handle any aspect ratio provided in the format `width:height`.

## Installation

```python
pip install real
```
## Usage

Here's a basic example of how to use the `Real` class:

```python
from real import Real

# Example usage
screen = Real(10, "16:9")
print(screen)

# get measurment individually
width = real.get_dimensions()["width"]
height = real.get_dimensions()["height"]
area = real.get_dimensions()["area"]
```


