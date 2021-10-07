# for pdf parsing
import fitz
import xml.etree.ElementTree as ET

# for docx parsing
import textract


def parse(file_path, extension):
    """
    Wrapper function to detect the file extension and call text
    extraction function accordingly

    :param file_path: path of file of which text is to be extracted
    :param extension: extension of file `file_name`
    :return:
    """
    lines = []
    if extension == '.pdf':
        lines = pdf_parser(file_path)
    elif extension == '.docx' or extension == '.doc':
        lines = doc_parser(file_path)

    # add Resume at the beginning of the doc
    # since most document start with the applicant name
    # when use spacy on that directly, space usually give a wrong pos tag for the name
    # add a prefix will help to solve the problem

    if lines:
        size, font, text = lines[0]
        lines[0] = size, font, "Resume: " + text
    return lines


def combine_lines(lines, longest_line):
    def find_first_letter(string):
        for l in string:
            if l.isalpha():
                return l
        else:
            return ""

    font_count = set([(font_size, font_name) for (font_size, font_name, text) in lines])
    # if font_count <= 1, the doc contains only one font, no further steps
    if len(font_count) <= 1000:
        return lines

    # if font_count > 1, it means the doc contains more than one font,  we can filter with those info
    LINE_DIFF = 10
    combined_lines = []
    for font_size, font_name, text in lines:
        first_letter = find_first_letter(text)
        if combined_lines and longest_line - len(combined_lines[-1]) > LINE_DIFF and first_letter.islower():
            combined_lines[-1] = (combined_lines[-1][0], combined_lines[-1][1], combined_lines[-1][2] + " "+text)
        else:
            combined_lines.append((font_size, font_name, text))

    return combined_lines


def pdf_parser(pdf_path):
    try:
        doc = fitz.open(pdf_path)

        lines = []
        for page in doc:
            page_xml = page.get_text("xml")
            # print(page_xml)
            tree = ET.ElementTree(ET.fromstring(page_xml))
            root = tree.getroot()

            for block in root:
                for line in block:
                    for font in line:
                        font_size = font.attrib['size']
                        font_name = font.attrib['name']

                        # jon chars
                        text = "".join([char.attrib['c'] for char in font])
                        text = text.strip()

                        # remove non alpha, non digital
                        if not text.lower().islower() and not any(map(str.isdigit, text)):
                            continue

                        lines.append((font_size, font_name, text))

        # find the longest line
        longest_line = max(len(text) for (font_size, font_name, text) in lines)

        # combine lines,
        # line 1: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        # line 2: nn
        # res   : aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaann
        combined_lines = combine_lines(lines, longest_line)

        return combined_lines
    except Exception:
        return []


def doc_parser(doc_path):
    font_size = 12
    font_name = "time"
    try:
        lines = []
        text = textract.process(doc_path).decode('utf-8')
        for line in text.split('\n'):
            line = line.strip()
            line.replace('\t', ' ')

            if not line:
                continue

            lines.append((font_size, font_name, line))

        longest_line = max(len(text) for (font_size, font_name, text) in lines)
        combined_lines = combine_lines(lines, longest_line)
        return combined_lines
    except KeyError:
        return []
