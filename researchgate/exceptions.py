# class AuthorizationFailedException(Exception):
#     def __str__(self):
#         return 'All authorization methods failed.'

class PageNotFoundException(Exception):
    def __init__(self, url: str = None):
        self.__url = url

    def __str__(self):
        if self.__url:
            return f'Page {self.__url} not found.'
        else:
            return f'Page not found.'


class LinkNotProvidedException(Exception):
    def __str__(self):
        return 'Link to the page is not provided'
