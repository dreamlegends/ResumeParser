import constants as cs
from textdistance import hamming, levenshtein


def parse(lines, nlp_text, matcher, job_titles, universities, skills, majors, email):
    email_names = extract_by_email(lines, email)
    if 1 < len(email_names) < 4:
        return " ".join(email_names)

    pattern_names = extract_by_pattern(nlp_text, matcher, job_titles, universities, skills, majors)
    if not pattern_names:
        return ""

    # filter by email names:
    if email_names:
        email_names = set(email_names)
        for can in pattern_names:
            for word in can.split(" "):
                if word in email_names:
                    return can

    # filter by email with hamming distance
    if email:
        email = email.split("@")[0].upper()
        for can in pattern_names:
            sim = hamming.normalized_similarity(email, can.upper())
            if sim == 0:
                continue
            return can

    return pattern_names[0]


def extract_by_email(lines, email):
    if not email:
        return []

    name = []

    email = email.split("@")[0].upper()

    for line in lines:
        for word in line.split(" "):
            if len(word) <= 1:
                continue

            if word.upper() in email:
                name.append(word)

    return name


def extract_by_pattern(nlp_text, matcher, job_titles, universities, skills, majors,):
    # find all none name phrase
    none_name_phrase = job_titles.union(universities).union(skills).union(majors)

    # The POS Tag for name usually proper noun, so first find all text with two proper nouns
    pattern = [cs.NAME_PATTERN]
    matcher.add('NAME', pattern)
    matches = matcher(nlp_text)

    # find all candidate
    candidates = []
    for _, start, end in matches:
        span = nlp_text[start:end].text

        if 'NAME' not in span.upper() and span.upper() not in none_name_phrase:
            candidates.append(span)

    return candidates
