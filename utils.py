def get_attibutes_to_match(source_tag):
    attributes_to_match = {}
    for attr, value in source_tag.attrs.items():
        if type(value) == list:
            value = ' '.join(value)
        attributes_to_match[attr] = value
    return attributes_to_match


def find_source_tag(source_html, source_id):
    tags = source_html.select(f'#{source_id}')
    if len(tags) == 0:
        raise ValueError(f'HTML doesnt contain tag with id = {source_id}')
    return tags[0]


def find_tag_by_text(html, text):
    tags = html.find_all(lambda tag: text in tag.text)
    return [] if len(tags) == 0 else [tags[-1]]


def get_matches_by_selector(diff_html, attributes_to_match, text_to_match):
    matches_by_selector = {}
    for attr, value in attributes_to_match.items():
        selector = f'{attr}="{value}"'
        matches_by_selector[selector] = diff_html.select(f'[{selector}]')

    matches_by_selector[f'text="{text_to_match}"'] = \
        find_tag_by_text(diff_html, text_to_match)
    return matches_by_selector


def get_matches_by_tag(matched_by_selector):
    matched_tags_acc = []
    for v in matched_by_selector.values():
        matched_tags_acc.extend(v)
    all_matched_tags = set(matched_tags_acc)

    matches_by_tag = {}
    for tag in all_matched_tags:
        matched_selectors = [selector for selector in matched_by_selector.keys()
                             if tag in matched_by_selector[selector]]
        matches_by_tag[tag] = matched_selectors
    return matches_by_tag