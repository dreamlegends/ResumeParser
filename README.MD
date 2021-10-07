# Resume Parser
------
![](https://img.shields.io/badge/build-passing-green.svg)
![](https://img.shields.io/badge/language-python-green.svg)
![](https://img.shields.io/badge/version-1.0-blue.svg)


## About
Resume Parser is a simple way for extracting information from Resumes.


## Installation & Requirement
* Install all the required packages in the requirements.txt file.
```shell
pip install -r requirments.txt
```
* You may want to install spacy NLP model package using the following command
```shell
python -m spacy download en_core_web_sm
```

## Use
Init a ResumeParser object and call parse function. A main function is in resume_parser.py
```python
parser = ResumeParser()
parser.parse("testing/testing_file/5.pdf")
```


## Sample Result Output
Return can either be Resume Object or a Json format string.
Here is an example for json string:
```json
{
   "name":"Hao Zhang",
   "email":"hao.joey.zhang@gmail.com",
   "mobile":"9782043357",
   "address":"110 Skyline Dr., Dracut, MA",
   "college_name":[
      "UNIVERSITY OF MASSACHUSETTS LOWELL",
      "TIANJIN UNIVERSITY OF TECHNOLOGY"
   ],
   "degree":[
      "MS COMPUTER SCIENCE",
      "PHD COMPUTER SCIENCE 2021",
      "BS COMPUTER SCIENCE 2011"
   ]
}
```

## TODOs
* Refine Section Segmentation Method
* Improve Name Detection with stanford NLP Core.
* Improve mobile extraction with general phone number regex (current support US)
* Add Experience Extractor
* Add Project Extractor
