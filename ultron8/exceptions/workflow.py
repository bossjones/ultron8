from __future__ import absolute_import

import logging

from ultron8 import exceptions as u8_exc
from ultron8.exceptions import db as db_exc

LOG = logging.getLogger(__name__)


def retry_on_exceptions(exc):
    LOG.warning("Determining if exception %s should be retried.", type(exc))

    retrying = isinstance(exc, db_exc.UltronDBObjectWriteConflictError)

    if retrying:
        LOG.warning("Retrying operation due to database write conflict.")

    return retrying


class WorkflowDefinitionException(u8_exc.UltronBaseException):
    pass


class WorkflowExecutionException(u8_exc.UltronBaseException):
    pass


class WorkflowExecutionNotFoundException(u8_exc.UltronBaseException):
    def __init__(self, ac_ex_id):
        Exception.__init__(
            self,
            "Unable to identify any workflow execution that is "
            'associated to action execution "%s".' % ac_ex_id,
        )


class AmbiguousWorkflowExecutionException(u8_exc.UltronBaseException):
    def __init__(self, ac_ex_id):
        Exception.__init__(
            self,
            "More than one workflow execution is associated "
            'to action execution "%s".' % ac_ex_id,
        )


class WorkflowExecutionIsCompletedException(u8_exc.UltronBaseException):
    def __init__(self, wf_ex_id):
        Exception.__init__(
            self, 'Workflow execution "%s" is already completed.' % wf_ex_id
        )


class WorkflowExecutionIsRunningException(u8_exc.UltronBaseException):
    def __init__(self, wf_ex_id):
        Exception.__init__(
            self, 'Workflow execution "%s" is already active.' % wf_ex_id
        )
