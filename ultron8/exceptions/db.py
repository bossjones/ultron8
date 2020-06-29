from ultron8.exceptions import UltronBaseException


class UltronDBObjectNotFoundError(UltronBaseException):
    pass


class UltronDBObjectMalformedError(UltronBaseException):
    pass


class UltronDBObjectConflictError(UltronBaseException):
    """
    Exception that captures a DB object conflict error.
    """

    def __init__(self, message, conflict_id, model_object):
        super(UltronDBObjectConflictError, self).__init__(message)
        self.conflict_id = conflict_id
        self.model_object = model_object


class UltronDBObjectWriteConflictError(UltronBaseException):
    def __init__(self, instance):
        msg = 'Conflict saving DB object with id "%s" and rev "%s".' % (
            instance.id,
            instance.rev,
        )
        super(UltronDBObjectWriteConflictError, self).__init__(msg)
