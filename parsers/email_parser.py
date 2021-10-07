import re


def parse(text):
    """
    Helper function to extract email from text
    :param text: plain text extracted from resume file
    :return:
    """
    email = re.findall(r"([^@|\s]+@[^@]+\.[^@|\s]+)", text)
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None
