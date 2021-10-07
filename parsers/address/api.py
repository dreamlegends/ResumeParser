from . import parser


def parse(some_text, **kwargs):
    """Creates request to AddressParser
    and returns list of Address objects
    """
    ap = parser.AddressParser(**kwargs)
    return ap.parse(some_text)
