from nltk.corpus import stopwords

# Hao Zhang
NAME_PATTERN = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

# Education (Upper Case Mandatory)
EDUCATION = [
            'BACHELOR', 'MASTER',
            'BE', 'B.E.', 'B.E', 'BACHELOR OF ENGINEERING',
            'BS', 'B.S.', 'B.S', 'BACHELOR OF SCIENCE',
            'ME', 'M.E.', 'M.E', 'MASTER OF ENGINEERING',
            'MS', 'M.S.', 'M.E', 'MASTER OF SCIENCE',
            'BTECH', 'B.TECH.', 'B.TECH', 'BACHELOR OF TECHNOLOGY',
            'MTECH', 'M.TECH.', 'M.TECH', 'MASTER OF TECHNOLOGY',
            'PHD', 'PH.D.', 'PH.D' 'DOCTOR OF PHILOSOPHY'
            'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII'
        ]

NOT_ALPHA_NUMERIC = r'[^a-zA-Z\d]'

NUMBER = r'\d+'

# For finding date ranges
MONTHS_SHORT = r'''(jan)|(feb)|(mar)|(apr)|(may)|(jun)|(jul)
                   |(aug)|(sep)|(oct)|(nov)|(dec)'''
MONTHS_LONG = r'''(january)|(february)|(march)|(april)|(may)|(june)|(july)|
                   (august)|(september)|(october)|(november)|(december)'''
MONTH = r'(' + MONTHS_SHORT + r'|' + MONTHS_LONG + r')'
YEAR = r'(((20|19)(\d{2})))'

STOPWORDS = set(stopwords.words('english'))

RESUME_SECTIONS_PROFESSIONAL = [
                    'experience',
                    'education',
                    'interests',
                    'professional experience',
                    'publications',
                    'skills',
                    'certifications',
                    'objective',
                    'career objective',
                    'summary',
                    'leadership',
                    'working experience',
                    'work experience',
                    'competencies',
                    'experiences',
                ]

RESUME_SECTIONS_GRAD = [
                    'accomplishments',
                    'experience',
                    'education',
                    'interests',
                    'projects',
                    'professional experience',
                    'publications',
                    'skills',
                    'certifications',
                    'objective',
                    'career objective',
                    'summary',
                    'leadership'
                    'working experience',
                    'work experience',
                    'competencies',
                    'experiences',
                ]
