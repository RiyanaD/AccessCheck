from bs4 import BeautifulSoup
import re
import math
import colorContrast

html_content = ''
def get_line_number(html_content, element):
    start = html_content.find(str(element)[:element.start_pos])
    line_number = html_content.count('\n', 0, start) + 1
    return line_number

# image alt
def detect_images_without_alt(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    images_without_alt = soup.find_all('img', alt=False) 

    if images_without_alt:
        img_tags_without_alt = []

        for img_tag in images_without_alt:
            img_tags_without_alt.append(str(img_tag))  # Convert img_tag to string

    return images_without_alt

# language

def detect_lang_attribute(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    html_element = soup.find('html')

    if html_element and 'lang' in html_element.attrs:
        return html_element['lang']
    else:
        return None
    
# form labels

def detect_missing_form_labels(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    form_elements = soup.find_all('form')
    elements_inside_form = []
    for form in form_elements:
        elements_inside_form.extend(form.find_all(['input', 'select', 'textarea', 'button']))

    missing_labels = []
    for element in elements_inside_form :
        if element.has_attr('id'):
            label = soup.find('label', {'for': element['id']})
            #if label doesn't exist or its text is empty 
            if not label or not label.text.strip():
                missing_labels.append(element)

    return missing_labels

def detect_undescriptive_link_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    a_tags = soup.find_all('a')
    non_descriptive_links = []
    for tag in a_tags:
        link_text = tag.text.strip()
        if not link_text:
            non_descriptive_links.append(tag)
        elif link_text.lower() in ['click here', 'here', 'link', 'read more', 'learn more']:
            non_descriptive_links.append(tag)

    return non_descriptive_links


def get_background_color(css_text):
    background_color_pattern = r'background-color:\s*(.*?);'

    background_color_match = re.search(background_color_pattern, css_text, re.IGNORECASE)

    if background_color_match:
        background_color_value = background_color_match.group(1)
        return background_color_value
    else:
        return None


# mainnnnn

def detect_data(param):
    html_content = param
    images_without_alt = detect_images_without_alt(html_content)
    lang_attribute_result = detect_lang_attribute(html_content)
    missing_labels = detect_missing_form_labels(html_content)
    non_descriptive_links = detect_undescriptive_link_text(html_content)
    #is_sufficient_color_contrast = colorContrast.detect_unsufficient_color_contrast(html_content)

    results = {}
    #only append to result if it exists, in tuple (description)
    if images_without_alt:
        images_without_alt_info = [] # list of dictionary elements{tag, line number}
        for element in images_without_alt:
            line_number = get_line_number(html_content, element)
            images_without_alt_info.append({"tag": str(element), "line_number": line_number})
        results["Image without alt attribute"] = images_without_alt_info
    else:
        results["Image without alt attribute"] = False
    
    if missing_labels:
        missing_labels_info = []
        for element in missing_labels:
            line_number = get_line_number(html_content, element)
            missing_labels_info.append({"tag": str(element), "line_number": line_number})
        results["Form element without corresponding label"] = missing_labels_info
    else:
        results["Form element without corresponding label"] = False

    if lang_attribute_result:
        results["lang attribute present in the HTML document."] = lang_attribute_result
    else:
        results["lang attribute present in the HTML document."] = False

    if non_descriptive_links:
        non_descriptive_links_info = []
        for element in non_descriptive_links:
            line_number = get_line_number(html_content, element)
            non_descriptive_links_info.append({"tag": str(element), "line_number": line_number})
        results["Non-descriptive links"] = non_descriptive_links_info
    else:
        results["Non-descriptive links"] = False
    
    # if is_sufficient_color_contrast:
    #     print(is_sufficient_color_contrast)
    # Combine the results and return them
    #result = f"{images_without_alt_result}"
    #result = f"{missing_labels_result}"
    #result = f"{lang_attribute_result}\n{images_without_alt_result}\n{missing_labels_result}"
    return results
