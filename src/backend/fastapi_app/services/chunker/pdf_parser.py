import pymupdf4llm
from unstructured.partition.md import partition_md
import json
import sys
from typing import List, Dict
from .section_checker import is_valid_header
from pprint import pprint


def pdf_parser():
    if len(sys.argv) < 2:
        print("Pdf file name required e.g. <arXiv_id>.pdf")
        return
    filename = sys.argv[1]

    pdf_path = f"./tmp_data/{filename}"
    result_json = pdf_to_json_pipeline(
        pdf_path
    )  # save_json set true for testing purpose
    # for r in result_json:
    #     print(r.get("header"))
    pprint(result_json)


def pdf_to_json_pipeline(pdf_path: str, save_json=False) -> Dict:
    """
    Converts a PDF to JSON via markdown conversion and section extraction.

    Args:
        pdf_path (str): Path to the input PDF file.
        save_json (bool, optional): Whether to save the output JSON to a file. Defaults to False.
    Returns:
        dict: JSON representation of the parsed content.
    """
    md_text = pdf_to_md(pdf_path)  # save_md set true for testing purpose
    dict_text = md_to_dict(md_text)
    if save_json:
        json_text = json.dumps(dict_text)
        with open(pdf_path.replace(".pdf", ".json"), "w") as f:
            f.write(json_text)
    return dict_text


def pdf_to_md(pdf_path: str, save_md=False) -> str:
    """
    Converts a PDF file to markdown text using pymupdf4llm.

    Args:
        pdf_path (str): Path to the input PDF file.
        save (bool, optional):  Whether to save the markdown output to a file. Defaults to False.

    Returns:
        str: Markdown content extracted from the PDF.
    """
    md_text = pymupdf4llm.to_markdown(pdf_path)
    if save_md:
        md_output_path = pdf_path.replace(".pdf", ".md")
        with open(md_output_path, "w") as f:
            f.write(md_text)
    return md_text


def md_to_dict(md_text: str, include_ref=False) -> List[Dict[str, str]]:
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
        element_str = str(element)
        # check for element marked as title/header and set as current title if valid
        if element.category in ["Title", "Header"] and "http" not in element_str:
            # terminate when the header name starts with reference
            if element_str.upper().startswith("REFERENCE") and not include_ref:
                break
            valid_header = is_valid_header(element_str, current_title)
            # check if the current title is a valid section header
            if valid_header:
                if current_title:
                    section_list.append(
                        {"header": current_title, "text": " ".join(current_text)}
                    )
                current_title = element_str
                current_text = []
            elif not valid_header and current_title:
                current_text.append(element_str)
                current_text.append(
                    "\n"
                )  # added for separating subsection/subsubsection name and paragraph
        # check for narrative text (paragraphs/sentences)
        # https://docs.unstructured.io/open-source/concepts/document-elements
        elif (
            element.category in ["NarrativeText", "UncategorizedText", "ListItem"]
            and current_title
        ):
            current_text.append(element_str)
    if current_title:
        section_list.append({"header": current_title, "text": " ".join(current_text)})
    return section_list


if __name__ == "__main__":
    pdf_parser()
