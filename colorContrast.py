import re
from bs4 import BeautifulSoup
import math

def get_background_color(element):
    # Traverse up the ancestor chain to find a parent element with a style attribute
    parent = element.parent
    while parent:
        if parent.has_attr('style'):
            # Extract the background-color property from the CSS styles
            background_color_match = re.search(r'background-color:\s*(.*?);', parent['style'], re.IGNORECASE)
            if background_color_match:
                return background_color_match.group(1)
        parent = parent.parent
    return None

def get_text_color(element):
    # Extract the style attribute from the element
    style_attribute = element.get('style')

    if style_attribute:
        # Use regular expression to find the value of the color property in the style attribute
        color_match = re.search(r'color:\s*(.*?);', style_attribute, re.IGNORECASE)
        if color_match:
            text_color = color_match.group(1)
            return text_color.strip()

    # If no style attribute or color property found, check the 'color' attribute directly
    if element.has_attr('color'):
        text_color = element['color']
        return text_color.strip()

    return None

def get_luminance(color):
    # Ensure that color values are in the range [0, 255]
    r, g, b = [c / 255.0 for c in color]
    if r <= 0.03928:
        R = r / 12.92
    else:
        R = ((r + 0.055) / 1.055) ** 2.4

    if g <= 0.03928:
        G = g / 12.92
    else:
        G = ((g + 0.055) / 1.055) ** 2.4

    if b <= 0.03928:
        B = b / 12.92
    else:
        B = ((b + 0.055) / 1.055) ** 2.4

    L = 0.2126 * R + 0.7152 * G + 0.0722 * B
    return L


def color_contrast_ratio(color1, color2):
    # Your implementation of color_contrast_ratio function
    luminance1 = get_luminance(color1)
    luminance2 = get_luminance(color2)

    if luminance1 < luminance2:
        luminance1, luminance2 = luminance2, luminance1

    contrast_ratio = (luminance1 + 0.05) / (luminance2 + 0.05)

    return contrast_ratio

def is_contrast_compliant(color1, color2, min_contrast_ratio):
    contrast_ratio = color_contrast_ratio(color1, color2)
    if (contrast_ratio >= min_contrast_ratio):
        return contrast_ratio
    return False

def detect_unsufficient_color_contrast(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text_elements = soup.find_all(text=True)
    text_background_colors = {}
    for element in text_elements:
        background_color = get_background_color(element)
        print("background color " + str(background_color))
        text_color = get_text_color(element)
        if background_color and text_color:
             colors_dict = {
                'background_color': background_color,
                'text_color': text_color
            }
        text_background_colors[element] = colors_dict

    text_without_sufficient_contrast = []
    if text_background_colors:
        for element, colors_dict in text_background_colors.items():
            contrast_ratio_normal_text = 4.5
            contrast_ratio_large_text = 3
            background_color = colors_dict['background_color']
            text_color = colors_dict['text_color']

            contrast_ratio = is_contrast_compliant(background_color, text_color, contrast_ratio_large_text)
            if (contrast_ratio):
                text_without_sufficient_contrast.append({"tag": str(element),"contrast_ratio": contrast_ratio})
    
    return text_without_sufficient_contrast


