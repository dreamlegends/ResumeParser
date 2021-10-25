import sys
import io
import os
import json
import pandas as pd
import spacy
import pickle
from spacy.matcher import Matcher
from parsers import email_parser, mobil_parser, address_parser, college_parser, degree_parser, doc_parser, section_parser, name_parser


class Resume:
    def __init__(self, **kwargs):
        self.name = None
        self.email = None
        self.mobile = None
        self.address = None
        self.college_name = None
        self.degree = None

        for k, v in kwargs.items():
            if k == "name":
                self.name = v
                break
            if k == "email":
                self.email = v
                break
            if k == "mobil":
                self.mobile = v
                break
            if k == "address":
                self.address = v
                break
            if k == "college_name":
                self.college_name = v
                break
            if k == "degree":
                self.degree = v
                break

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'mobile': self.mobile,
            'address': self.address,
            'college_name': self.college_name,
            'degree': self.degree,
        }

    def to_json(self):
        dct = self.to_dict()
        return json.dumps(dct)


class ResumeParser:
    COLLEGE_SET_FILE = 'info/universities.csv'
    SKILL_SET_FILE = 'info/skills.csv'
    MAJOR_SET_FILE = 'info/majors.csv'
    JOB_SET_FILE = 'info/jobtitles.csv'

    def __init__(self, skill_set=None, college_set=None, major_set=None, job_set=None):
        self.nlp = spacy.load('en_core_web_sm')
        self.matcher = Matcher(self.nlp.vocab)
        self.skills = skill_set if skill_set else self._load_skills()
        self.colleges = college_set  if college_set else self._load_colleges()
        self.majors = major_set if major_set else self._load_majors()
        self.jobs = job_set if job_set else self._load_jobs()

    @staticmethod
    def _load_colleges():
        """
        :return: a set of colleges
        """
        data = pd.read_csv(ResumeParser.COLLEGE_SET_FILE)

        colleges = list(data.name)  # full list of colleges
        colleges = [college.upper() for college in colleges]

        # some alternative names
        colleges += [college.replace(" AT ", " ") for college in colleges if ' AT ' in college]
        colleges += [college.replace(" AT ", ", ") for college in colleges if ' AT ' in college]

        return set(colleges)

    @staticmethod
    def _load_skills():
        """
        :return: a set of skills
        """
        skills_df = pd.read_csv(ResumeParser.SKILL_SET_FILE)
        skills = list(skills_df.columns.values)
        return set(skill.upper() for skill in skills)

    @staticmethod
    def _load_majors():
        majors_df = pd.read_csv(ResumeParser.MAJOR_SET_FILE)
        majors = list(majors_df.Major)
        return set(major.upper() for major in majors)

    @staticmethod
    def _load_jobs():
        title_df = pd.read_csv(ResumeParser.JOB_SET_FILE)
        titles = list(title_df.Title.values)
        return set(title.upper() for title in titles)

    @staticmethod
    def save(path):
        """
        save a ResumeParser Object
        """
        parser = ResumeParser()
        with open(path, 'wb') as handle:
            pickle.dump(parser, handle, protocol=pickle.HIGHEST_PROTOCOL)
        return

    @staticmethod
    def load(path):
        """
        load a ResumeParser Object
        """
        with open(path, 'rb') as handle:
            resume_obj = pickle.load(handle)
        return resume_obj

    def parse(self, resume, return_type="str"):
        """
        :param resume: resume input can be a file location, or bytesIO
        :param return_type:
            str -> return json string
            obj -> return Resume object
        :return:
        """
        # extract extension
        if not isinstance(resume, io.BytesIO):
            ext = os.path.splitext(resume)[1].split('.')[1]
        else:
            ext = resume.name.split('.')[1]

        # extract text
        # each line in the resume contains font size, font name, text
        formatted_text = doc_parser.parse(resume, '.' + ext)

        resume = Resume()
        if formatted_text:
            # separate text in sections
            sections = section_parser.parse(formatted_text)

            # turn each section text in to pure text and a spacy object
            section_raw_text = {key: "\n".join([text.strip() for font_size, font_name, text in section]) for key, section in sections.items()}

            sections_nlp = {key: self.nlp(text) for key, text in section_raw_text.items()}

            raw_text = "\n".join([text for (font_size, font_name, text) in formatted_text])

            email = ""
            if "beginning" in section_raw_text:
                email = email_parser.parse(section_raw_text['beginning'])
            if not email:
                email = email_parser.parse(raw_text)

            mobil = ""
            if "beginning" in section_raw_text:
                mobil = mobil_parser.parse(section_raw_text['beginning'])
            if not mobil:
                mobil = mobil_parser.parse(raw_text)

            address = None
            if "beginning" in section_raw_text:
                address = address_parser.parse(section_raw_text['beginning'])
            if not address:
                address = address_parser.parse(raw_text)
            address = address.get_full_address() if address else ""

            colleges = []
            if "education" in section_raw_text:
                colleges = college_parser.parse([text.strip() for font_size, font_name, text in sections['education']], self.colleges)
            if not colleges:
                colleges = college_parser.parse([text.strip() for font_size, font_name, text in formatted_text], self.colleges)

            degree = []
            if "education" in section_raw_text:
                degree = degree_parser.parse([text.strip() for font_size, font_name, text in sections['education']], self.majors)
            if not degree:
                degree = degree_parser.parse([text.strip() for font_size, font_name, text in formatted_text], self.majors)

            name = ""
            if "beginning" in section_raw_text:
                name = name_parser.parse([text.strip() for font_size, font_name, text in sections['beginning']],
                                         sections_nlp['beginning'],
                                         self.matcher, self.jobs, self.colleges, self.skills, self.majors, email)
            if not name:
                name = name_parser.parse([text.strip() for font_size, font_name, text in formatted_text],
                                         self.nlp(raw_text),
                                         self.matcher, self.jobs, self.colleges, self.skills, self.majors, email)

            resume.email = email
            resume.mobile = mobil
            resume.address = address
            resume.college_name = colleges
            resume.degree = degree
            resume.name = name

        if return_type == "str":
            return resume.to_json()
        else:
            return Resume


if __name__ == "__main__":
    # new init method
    MODEL_PATH = sys.argv[2] + "/ResumeParser/models/resume_model.pickle"
    parser = ResumeParser.load(MODEL_PATH)
    print(parser.parse(sys.argv[1]))
