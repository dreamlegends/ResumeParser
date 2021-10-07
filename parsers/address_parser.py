from parsers.address.parser import AddressParser


def parse(text, country='US'):
    """
    borrowed this from pyap package, https://github.com/vladimarius/pyap

    :param text:
    :param country:
    :return:
    """
    parser = AddressParser(country=country)
    addresses = parser.parse(text)
    for address in addresses:
        if address:
            return address
