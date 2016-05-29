from __future__ import unicode_literals

class BadDataError(ValueError):
    pass

class ContentTypeError(BadDataError):
    def __init__(self, content_type):
        self.content_type = content_type
        self.message = "Unknown Content-Type {}".format(repr(content_type))
    def __str__(self):
        return self.message
    def __repr__(self):
        return "ContentTypeError({})".format(repr(self.content_type))

