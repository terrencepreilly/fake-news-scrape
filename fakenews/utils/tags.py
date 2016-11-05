import re

TAGS = re.compile('<.+?>')


def extract_paragraphs(all_ps):
    """Extract the inner html from all the paragraphs, and remove tags.

    Args:
        p_tags: A set of paragraph tags.
    Returns: The text of the paragraph tags, without any tags.
    """
    text = ''
    for p in all_ps:
        curr = p.extract()
        if isinstance(curr, str):
            text += ' '.join(TAGS.split(curr))
    return text
