import re


def parse(lines, colleges_set):
    """
    Helper function to extract college names
    :param lines: string list each string is a line
    :param colleges_set: a set of colleges
    :return: list of college names
    """
    college_reg = re.compile(r'[.]*(College|University|Institute|Law School|School of|Academy)[.]*', re.IGNORECASE)

    # find the candidate line from the input text
    college_lst = []
    for line in lines:
        find = re.findall(college_reg, line)
        if find:
            college_lst.append(line)
    nlp_text_sents = college_lst

    matched_university = []
    for sent in nlp_text_sents:
        # find candidate
        # if the college name in current line then the college is a candidate
        # this may raise a problem:
        # example: Beijing University of Technology  -> candidate: Beijing University, Beijing University of Technology
        candidates = [col for col in colleges_set if col.upper() in sent.upper()]

        # continue if found nothing
        if not candidates:
            continue

        # if find multiple candidate return the one that has the longest match, see prev problem for detail
        if len(candidates) > 1:
            candidates = [max(candidates, key=len)]

        matched_university.append(candidates[0])

    return matched_university
