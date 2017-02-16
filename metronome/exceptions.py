class MetronomeError(Exception):
    pass


class MetronomeHttpError(MetronomeError):

    def __init__(self, response):
        """
        :param :class:`requests.Response` response: HTTP response
        """
        self.error_message = response.reason or ''
        if response.content:
            content = response.json()
            self.error_message = content.get('message', self.error_message)
            self.error_details = content.get('details')
        self.status_code = response.status_code
        super(MetronomeHttpError, self).__init__(self.__str__())

    def __repr__(self):
        return 'MetronomeHttpError: HTTP %s returned with message, "%s"' % \
               (self.status_code, self.error_message)

    def __str__(self):
        return self.__repr__()


class NotFoundError(MetronomeHttpError):
    pass


class InternalServerError(MetronomeHttpError):
    pass


class InvalidChoiceError(MetronomeError):

    def __init__(self, param, value, options):
        super(InvalidChoiceError, self).__init__(
            'Invalid choice "{value}" for param "{param}". Must be one of {options}'.format(
                param=param, value=value, options=options
            )
        )
