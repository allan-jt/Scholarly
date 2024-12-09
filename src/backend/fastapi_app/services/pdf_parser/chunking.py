import pymupdf4llm
from unstructured.partition.md import partition_md
from unstructured.documents.elements import Element
import re
import json
import sys

REFERECE_SECTION = "REFERENCE"
NUMERAL_HEADER_REGEX = r"^\d+[\.\s]+[A-Za-z0-9\s?]+" # Starts with a number followed by alphanum or ./?/space/
ROMAN_NUM_HEADER_REGEX = r"^(X{0,2}(IX|IV|V?I{0,3}))\b[\s.]+[A-Za-z0-9]" # Roman numerals up to 20
HEADER_REGEX = re.compile(f"{NUMERAL_HEADER_REGEX}|{ROMAN_NUM_HEADER_REGEX}")

def main():    
    if len(sys.argv) < 2:
        print("Pdf file name required e.g. <arXiv_id>.pdf")
        return
    filename = sys.argv[1]
    
    pdf_path = f"./tmp_data/{filename}"
    pdf_to_json_pipeline(pdf_path, save_json=True)

def pdf_to_json_pipeline(pdf_path: str, save_json=False):
    """
    Converts a PDF to JSON via markdown conversion and section extraction.
    
    Args:
        pdf_path (str): Path to the input PDF file.
        save_json (bool, optional): Whether to save the output JSON to a file. Defaults to False.
    Returns:
        str: JSON representation of the parsed content.
    """
    md_text = pdf_to_md(pdf_path, True)
    dict_text = md_to_dict(md_text)
    json_text = json.dumps(dict_text)
    if save_json:
        with open(pdf_path.replace(".pdf", ".json"), 'w') as f:   
            f.write(json_text)
    return json_text

def md_to_dict(md_text: str, include_ref=False):
    """
    Converts markdown text into a list of sections with headers and content.

    Args:
        md_text (str): Markdown content to parse.
        include_ref (bool, optional): Whether to include the reference section. Defaults to False.

    Returns:
        List[Dict[str, str]]: A list of sections with headers and content.
    """
    elements = partition_md(text=md_text)
    current_title = None
    current_text = []
    section_list = []
    for element in elements:
        # element_str = remove_citations(element)
        element_str = str(element)
        if element.category in ["Title", "Header"] and "http" not in element_str:
            if element_str.upper().startswith(REFERECE_SECTION) and not include_ref:
                break
            if is_valid_header(element_str, current_title): 
                if current_title:
                    section_list.append({
                        "header": current_title,
                        "text": ' '.join(current_text)
                    })
                current_title = element_str
                current_text = []
        elif element.category in ["NarrativeText"] and current_title:
            current_text.append(element_str)
    if current_title:
        section_list.append({
            "header": current_title,
            "text": ' '.join(current_text)
        })
    return section_list

def pdf_to_md(pdf_path: str, save=False):
    """
    Converts a PDF file to markdown text using pymupdf4llm.

    Args:
        pdf_path (str): Path to the input PDF file.
        save (bool, optional):  Whether to save the markdown output to a file. Defaults to False.

    Returns:
        str: Markdown content extracted from the PDF.
    """
    md_text = pymupdf4llm.to_markdown(pdf_path)
    if save:
        md_output_path = pdf_path.replace(".pdf", ".md")
        with open(md_output_path, "w") as f:
            f.write(md_text)
    return md_text

def is_valid_header(new_header: str, prev_header: str):
    """
    Validates if a new header is a valid successor to the previous one.

    Args:
        new_header (str): New section header.
        prev_header (str): Previous section header.

    Returns:
        bool: True if the new header is valid, False otherwise.
    """
    if not HEADER_REGEX.match(new_header):
        return False
    if prev_header is None:
        return True
    new_header = parse_roman_numeral(new_header)
    prev_header = parse_roman_numeral(prev_header)
    new_section_num = extract_section_number(new_header)
    prev_section_num = extract_section_number(prev_header)
    return new_section_num > prev_section_num

def parse_roman_numeral(header: str):
    """
    Converts Roman numerals in the header to integers.

    Args:
        header (str): Header string to process.

    Returns:
        str: Header with Roman numerals replaced by integers.
    """
    match = re.match(ROMAN_NUM_HEADER_REGEX, header)
    if match:
        roman_numeral = match.group(1)
        integer_value = roman_to_int(roman_numeral)
        return f"{integer_value}{header[len(roman_numeral):]}"
    return header

def extract_section_number(header: str):
    """
    Extracts a numeric or decimal section number from a header.

    Args:
        header (str): Header string to parse.

    Returns:
        Optional[float]: Extracted section number, or None if not found.
    """
    match = re.search(r"^\d+(\.\d+)?", header)
    return float(match.group()) if match else None

def roman_to_int(roman_str: str):
    """
    Converts a Roman numeral string to an integer.

    Args:
        roman_str (str): Roman numeral string.

    Returns:
        int: Integer representation of the Roman numeral.
    """
    roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    prev_value = 0
    for char in reversed(roman_str):
        value = roman_map.get(char, 0)
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value
    return total

# def remove_citations(element: Element):
#     remove_citations = lambda text: re.sub("\[\d{1,3}\]", "", text)
#     element.apply(remove_citations)
#     element_str = str(element).strip()
#     return element_str

if __name__ == "__main__":
    main()