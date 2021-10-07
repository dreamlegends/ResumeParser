import re
import constants as cs
from collections import defaultdict


def parse(lines, majors):
    edu = defaultdict(str)
    try:
        prev_degree = ""
        for index, line in enumerate(lines):
            # remove punctuation
            line = re.sub(r'[?|$|.|!|,]', r'', line)

            word_set = set(line.upper().split(" "))

            # for each degree, we want to check if the degree text in current line
            add_flag = False
            for degree in cs.EDUCATION:
                if degree in line.upper() and line not in cs.STOPWORDS:

                    # degree can be BE, BS -> this can be easily found in a text string
                    # thus, we need to make sure that every word in degree is in the line word set
                    flag = True
                    for w in degree.split(" "):
                        # could not find a word
                        if w not in word_set:
                            flag = False

                    # add degree and add the line of text to it.
                    if flag:
                        edu[degree] += line
                        add_flag = True
                        prev_degree = degree

            # can not find any new degree, so add current line to the previous degree.
            if not add_flag and prev_degree in edu:
                edu[prev_degree] += " \n " + line
    except IndexError:
        pass

    # Extract major & year
    # major and year usually stay behind the degree
    # we found every line behind the degree, so now lets search it.
    education = []
    for key, followed_text in edu.items():
        edu_info = [key]

        # check if any major and year info in the followed text
        major = [major for major in majors if major in followed_text.upper()]
        if major:
            edu_info.append(major[0])

        year = re.search(re.compile(cs.YEAR), followed_text)
        if year:
            edu_info.append(''.join(year.group(0)))

        # append to res
        education.append(' '.join(edu_info))
    return education
