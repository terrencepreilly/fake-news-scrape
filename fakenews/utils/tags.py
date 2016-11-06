import re

TAGS = re.compile('<.+?>')


def extract_paragraphs(all_ps, as_list=False):
    """Extract the inner html from all the paragraphs, and remove tags.

    Args:
        p_tags: A set of paragraph tags.
    Returns: The text of the paragraph tags, without any tags.
    """
    text = [] if as_list else ''
    for p in all_ps:
        curr = p.extract()
        if isinstance(curr, str):
            if as_list:
                text += [' '.join(TAGS.split(curr))]
            else:
                text += ' '.join(TAGS.split(curr))
    return text
