from __future__ import absolute_import

from ultron8 import exceptions as u8_exc
import logging


LOG = logging.getLogger(__name__)


class InvalidInquiryInstance(u8_exc.UltronBaseException):
    def __init__(self, inquiry_id):
        Exception.__init__(
            self, 'Action execution "%s" is not an inquiry.' % inquiry_id
        )


class InquiryTimedOut(u8_exc.UltronBaseException):
    def __init__(self, inquiry_id):
        Exception.__init__(
            self, 'Inquiry "%s" timed out and cannot be responded to.' % inquiry_id
        )


class InquiryAlreadyResponded(u8_exc.UltronBaseException):
    def __init__(self, inquiry_id):
        Exception.__init__(
            self, 'Inquiry "%s" has already been responded to.' % inquiry_id
        )


class InquiryResponseUnauthorized(u8_exc.UltronBaseException):
    def __init__(self, inquiry_id, user):
        msg = 'User "%s" does not have permission to respond to inquiry "%s".'
        Exception.__init__(self, msg % (user, inquiry_id))


class InvalidInquiryResponse(u8_exc.UltronBaseException):
    def __init__(self, inquiry_id, error):
        msg = 'Response for inquiry "%s" did not pass schema validation. %s'
        Exception.__init__(self, msg % (inquiry_id, error))
