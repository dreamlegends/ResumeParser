import re


def parse(text):
    """
    Helper function to extract mobile number from text

    :param text: plain text extracted from resume file
    :return: string of extracted mobile number
    """
    mob_num_regex = r'((?:(?<![\d-])(?:\+?\d{1,3}[-.\s*]?)?(?:\(?\d{3}\)?[-.\s*]?)?\d{3}[-.\s*]?\d{4}(?![\d-]))|(?:(?<![\d-])(?:(?:\(\+?\d{2}\))|(?:\+?\d{2}))\s*\d{2}\s*\d{3}\s*\d{4}(?![\d-])))'
    phone = re.findall(re.compile(mob_num_regex), text)

    if phone:
        number = ''.join(phone[0])
        num_only = "".join([d for d in number if d.isdigit()])
        return "+" + num_only if "+" in number else num_only
