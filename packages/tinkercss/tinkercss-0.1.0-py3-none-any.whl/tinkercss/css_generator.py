class TinkerCSS:
    def __init__(self):
        self.styles = {}

    def add_style(self, property_name, value):
        """Adds a style property and value to the style dictionary."""
        self.styles[property_name] = value

    def set_background(self, color):
        """Sets the background color."""
        self.add_style('background-color', color)
        return self

    def set_font_size(self, size):
        """Sets the font size."""
        self.add_style('font-size', size)
        return self

    def set_margin(self, margin):
        """Sets the margin."""
        self.add_style('margin', margin)
        return self

    def set_padding(self, padding):
        """Sets the padding."""
        self.add_style('padding', padding)
        return self

    def set_border(self, border):
        """Sets the border."""
        self.add_style('border', border)
        return self

    def generate_css(self):
        """Generates the CSS string."""
        return '; '.join([f"{key}: {value}" for key, value in self.styles.items()]) + ';'
