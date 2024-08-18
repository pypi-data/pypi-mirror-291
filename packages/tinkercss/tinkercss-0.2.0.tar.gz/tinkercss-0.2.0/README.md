# TinkerCSS

TinkerCSS is a Python library for generating CSS in a Tinker-like style. It allows you to create CSS styles using a Pythonic interface.

## Installation

You can install TinkerCSS via pip:

```bash
pip install tinkercss
```

## Example

```python
from tinkercss import TinkerCSS

style = TinkerCSS()
css_code = (
    style.set_background('blue')
         .set_font_size('16px')
         .set_margin('10px')
         .set_padding('5px')
         .set_border('1px solid black')
         .generate_css()
)

print(css_code)
```
