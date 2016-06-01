from six import text_type

class BadDataError(ValueError):
    pass

class ContentTypeError(BadDataError):
    def __init__(self, content_type):
        # type: (text_type) -> None
        self.content_type = content_type
        self.message = "Unknown Content-Type {}".format(repr(content_type))

    def __str__(self):
        # type: () -> str
        return self.message

    def __repr__(self):
        # type: () -> str
        return "ContentTypeError({})".format(repr(self.content_type))

