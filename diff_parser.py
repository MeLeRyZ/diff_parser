import os
import sys

from bs4 import BeautifulSoup

from defaults import DEFAULT_TAG_ID
from utils import *


def get_matches(source_file, diff_file, source_id):
    if not os.path.exists(source_file) and not os.path.exists(diff_file):
        raise ValueError("Files doesn't exist")

    with open(source_file) as f:
        source_html = BeautifulSoup(f, 'html.parser')

    source_tag = find_source_tag(source_html, source_id)
    tag_text = source_tag.text.strip() 
    tag_attributes = get_attibutes_to_match(source_tag)
    
    with open(diff_file) as f:
        diff_html = BeautifulSoup(f, 'html.parser')

    matched_by_selector = get_matches_by_selector(diff_html, tag_attributes, tag_text)
    matched_tags = get_matches_by_tag(matched_by_selector)

    matched_tag = max(matched_tags, key=lambda tag: len(matched_tags[tag]))
    output = get_output(matched_tag)
    return matched_tag, output


if __name__ == '__main__':
    source_file = sys.argv[1]
    diff_file = sys.argv[2]
    source_id = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_TAG_ID

    matched_tag, output = get_matches(source_file, diff_file, source_id)
    print(f"\nMatched tag:\n\n ```\n{matched_tag}\n```\n\nTag tree: {output}\n\nThank you!")