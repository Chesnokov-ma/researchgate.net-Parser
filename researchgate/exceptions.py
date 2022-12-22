# class AuthorizationFailedException(Exception):
#     def __str__(self):
#         return 'All authorization methods failed.'

class PageNotFoundException(Exception):
    def __str__(self):
        return 'Page not found.'
