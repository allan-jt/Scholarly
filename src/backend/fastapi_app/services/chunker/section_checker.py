import re
from typing import Optional

NUMERAL_HEADER_REGEX = r"^\d+[\.\s]+[A-Za-z0-9\s?]+" # Starts with a number followed by alphanum or ./?/space/
ROMAN_NUM_HEADER_REGEX = r"^(X{0,2}(IX|IV|V?I{0,3}))\b[\s.]+[A-Za-z0-9]" # Roman numerals up to 20
HEADER_REGEX = re.compile(f"{NUMERAL_HEADER_REGEX}|{ROMAN_NUM_HEADER_REGEX}")

def is_valid_header(new_header: str, prev_header: str) -> bool:
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

def parse_roman_numeral(header: str) -> str:
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

def extract_section_number(header: str) -> Optional[float]:
    """
    Extracts a numeric or decimal section number from a header.

    Args:
        header (str): Header string to parse.

    Returns:
        Optional[float]: Extracted section number, or None if not found.
    """
    match = re.search(r"^\d+(\.\d+)?", header)
    return float(match.group()) if match else None

def roman_to_int(roman_str: str) -> int:
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