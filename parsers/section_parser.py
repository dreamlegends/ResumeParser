import constants as cs
from collections import Counter
import unicodedata


def parse(formated_text_lst):
    """
    Helper function to extract all the raw text from sections of
    resume specifically for graduates and undergraduates
    :param text: Raw text of resume
    :return: dictionary of entities
    """
    # find the most common text format
    font_counter = Counter([(font_size, font_name) for (font_size, font_name, text) in formated_text_lst])
    mc_font_size, mc_font_name = font_counter.most_common(1)[0][0]

    section_names = {}
    for i, (font_size, font_name, text) in enumerate(formated_text_lst):

        # if the document has multiple font, the filter by font first
        if len(font_counter) > 1:
            # if cur_line format == common format then its not a section
            if font_size == mc_font_size and font_name == mc_font_name:
                continue

        # find section info based on matching
        p_key = set(text.lower().split()) & set(cs.RESUME_SECTIONS_GRAD)
        if p_key:
            section_names[i] = p_key

    sections = {'beginning': []}
    key = 'beginning'
    for i, (font_size, font_name, text) in enumerate(formated_text_lst):
        # unicode normalize, remove type of spaces, characters
        text = unicodedata.normalize("NFKD", text)

        if i not in section_names:
            sections[key].append((font_size, font_name, text))
        else:
            key = " ".join(list(section_names[i]))
            if key in sections:
                key += " others"

                # we may have 3 conflict
                # exp, exp, exp
                # the second one will be called exp others
                # for the third one, it will just add to others.
                # exp, exp_other, exp_other
                if key not in sections:
                    sections[key] = []
            else:
                sections[key] = []
            sections[key].append((font_size, font_name, text))

    return sections
