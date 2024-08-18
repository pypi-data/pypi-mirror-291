# tinkercss/css_generator.py

import tkinter as tk

class TinkerCSS:
    def __init__(self):
        self.styles = {}

    def add_style(self, property_name, value):
        """Adds a style property and value to the style dictionary."""
        self.styles[property_name] = value
        return self

    def set_background(self, color):
        """Sets the background color."""
        return self.add_style('background', color)

    def set_color(self, color):
        """Sets the text color."""
        return self.add_style('color', color)

    def set_font_family(self, font_family):
        """Sets the font family."""
        return self.add_style('font-family', font_family)

    def set_font_size(self, size):
        """Sets the font size."""
        return self.add_style('font-size', size)

    def set_margin(self, margin):
        """Sets the margin."""
        return self.add_style('margin', margin)

    def set_padding(self, padding):
        """Sets the padding."""
        return self.add_style('padding', padding)

    def set_border(self, border):
        """Sets the border."""
        return self.add_style('border', border)

    def generate_css(self):
        """Generates the CSS string."""
        return '; '.join([f"{key}: {value}" for key, value in self.styles.items()]) + ';'

    def apply_to_widget(self, widget):
        """
        Apply the stored styles to a Tkinter widget.

        :param widget: The Tkinter widget to which styles will be applied.
        """
        for key, value in self.styles.items():
            if key == 'background':
                widget.config(bg=value)
            elif key == 'color':
                widget.config(fg=value)
            elif key == 'font-family':
                current_font = widget.cget('font').split()[1] if len(widget.cget('font').split()) > 1 else '12'
                widget.config(font=(value, current_font))
            elif key == 'font-size':
                current_font = widget.cget('font').split()[0]
                widget.config(font=(current_font, value))
            elif key == 'border':
                # tkinter nespēj apstrādāt border tieši
                # izmantot citu pieeju, ja nepieciešams
                pass
            elif key == 'padding':
                # Padding tiek sadalīts pa vertikāli un horizontāli
                padding_values = value.split()
                if len(padding_values) == 1:
                    widget.config(padx=padding_values[0], pady=padding_values[0])
                elif len(padding_values) == 2:
                    widget.config(padx=padding_values[0], pady=padding_values[1])
            elif key == 'margin':
                # Margin nav tieši atbalstīts tkinter
                # Piemērot margin atsevišķi, ja nepieciešams
                pass

        # Var būt nepieciešams pārdomāt un pievienot papildu funkcionalitāti, piemēram, border-radius utt.
