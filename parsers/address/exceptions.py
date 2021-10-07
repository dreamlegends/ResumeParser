class AddressParserException(Exception):
    pass


class NoCountrySelected(AddressParserException):
    ''' No country selected during module initialization '''
    def __init__(self, message, errors):
        super(NoCountrySelected, self).__init__(message)
        self.errors = errors


class CountryDetectionMissing(AddressParserException):
    ''' Country-specific address detection rules were not found '''
    def __init__(self, message, errors):
        super(CountryDetectionMissing, self).__init__(message)
        self.errors = errors
