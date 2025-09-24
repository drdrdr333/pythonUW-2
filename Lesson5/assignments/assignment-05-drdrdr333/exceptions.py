''' Exceptions for our first assignment '''

class NonFileExtension(Exception):
    ''' For inaccurate or non-existent file
        extenstions
    '''
    pass


class InvalidEmailException(Exception):
    ''' For non-regex conforming email
    '''
    pass