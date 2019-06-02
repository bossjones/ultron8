"""Base classes and helpers for unit tests."""
try:
    from unittest import mock
except ImportError:
    import mock

# from unittest.mock import patch, MagicMock, Mock
import ultron8
import json as jsonlib
import os.path
import sys
import pytest
import unittest
import logging
from ultron8.consts import YAML_FILE
from ultron8.yaml import yaml, yaml_load, yaml_save, yaml_dump_roundtrip

from io import StringIO

LOGGER = logging.getLogger(__name__)


def get_parent_dir():
    """
    Gets the ultron8 root directory.
    """
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.join(tests_dir, os.path.pardir, "..")
    return os.path.abspath(parent_dir)


def get_test_config_dir(*add_path):
    """Return a path to a test config dir."""
    return os.path.join(os.path.dirname(__file__), "testing_config", *add_path)


def create_url_helper(base_url):
    """A function to generate ``url_for`` helpers."""
    base_url = base_url.rstrip("/")

    def url_for(path=""):
        if path:
            path = "/" + path.strip("/")
        return base_url + path

    return url_for


def create_example_data_helper(example_filename):
    """A function to generate example data helpers."""
    directory = os.path.dirname(__file__)
    directory = os.path.join(directory, "fixtures")
    example = os.path.join(directory, "{}{}".format(example_filename, YAML_FILE))

    def data_helper():
        data = yaml_load(example, ordered=True)
        return data

    return data_helper


def example_data_to_str(example_filename):
    """Load a fixture file on disk into memory, create object, then dump it as a string."""
    get_config_example_data = create_example_data_helper(example_filename)
    example_data = get_config_example_data()

    return yaml_dump_roundtrip(example_data)


# def build_url(self, *args, **kwargs):
#     """A function to proxy to the actual UltronSession#build_url method."""
#     # We want to assert what is happening with the actual calls to the
#     # Internet. We can proxy this.
#     return ultron8.session.UltronSession().build_url(*args, **kwargs)


# class UnitHelper(unittest.TestCase):
#     """Base class for unittests."""

#     # Sub-classes must assign the class to this during definition
#     described_class = None
#     # Sub-classes must also assign a dictionary to this during definition
#     example_data = {}

#     @staticmethod
#     def get_build_url_proxy():
#         return build_url

#     def create_mocked_session(self):
#         """Use mock to auto-spec a UltronSession and return an instance."""
#         MockedSession = mock.create_autospec(ultron8.session.UltronSession)
#         return MockedSession()

#     def create_session_mock(self, *args):
#         """Create a mocked session and add headers and auth attributes."""
#         session = self.create_mocked_session()
#         base_attrs = ["headers", "auth"]
#         attrs = dict((key, mock.Mock()) for key in set(args).union(base_attrs))
#         session.configure_mock(**attrs)
#         session.delete.return_value = None
#         session.get.return_value = None
#         session.patch.return_value = None
#         session.post.return_value = None
#         session.put.return_value = None
#         session.has_auth.return_value = True
#         return session

#     def create_instance_of_described_class(self):
#         """
#         Use cls.example_data to create an instance of the described class.

#         If cls.example_data is None, just create a simple instance of the
#         class.
#         """
#         if self.example_data and self.session:
#             instance = self.described_class(self.example_data, self.session)
#         elif self.example_data and not self.session:
#             session = self.create_session_mock()
#             instance = self.described_class(self.example_data, session)

#         else:
#             instance = self.described_class(session=self.session)

#         return instance

#     def delete_called_with(self, *args, **kwargs):
#         """Use to assert delete was called with JSON."""
#         self.method_called_with("delete", args, kwargs)

#     def method_called_with(self, method_name, args, kwargs):
#         """Assert that a method was called on a session with JSON."""
#         mock_method = getattr(self.session, method_name)
#         assert mock_method.called is True
#         call_args, call_kwargs = mock_method.call_args

#         using_json = False
#         # Data passed to assertion
#         data = kwargs.pop("data", None)
#         if data is None:
#             using_json = True
#             data = kwargs.pop("json", None)
#         # Data passed to patch
#         call_data = call_kwargs.pop("json" if using_json else "data", None)
#         # Data passed by the call to post positionally
#         #                                URL, 'json string'
#         if data and call_data is None:
#             call_args, call_data = call_args[:1], call_args[1]
#         # If data is a dictionary (or list) and call_data exists
#         if not isinstance(data, str) and call_data:
#             if not using_json:
#                 call_data = jsonlib.loads(call_data)

#         assert args == call_args
#         assert data == call_data
#         assert kwargs == call_kwargs

#     def patch_called_with(self, *args, **kwargs):
#         """Use to assert patch was called with JSON."""
#         self.method_called_with("patch", args, kwargs)

#     def post_called_with(self, *args, **kwargs):
#         """Use to assert post was called with JSON."""
#         assert self.session.post.called is True
#         call_args, call_kwargs = self.session.post.call_args

#         # Data passed to assertion
#         data = kwargs.pop("data", None)
#         # Data passed by the call to post positionally
#         #                                URL, 'json string'
#         call_args, call_data = call_args[:1], call_args[1]
#         # If data is a dictionary (or list) and call_data exists
#         if not isinstance(data, str) and call_data:
#             call_data = jsonlib.loads(call_data)

#         assert args == call_args
#         assert data == call_data
#         assert kwargs == call_kwargs

#     def put_called_with(self, *args, **kwargs):
#         """Use to assert put was called with JSON."""
#         self.method_called_with("put", args, kwargs)

#     def setUp(self):
#         """Use to set up attributes on self before each test."""
#         self.session = self.create_session_mock()
#         # Proxy the build_url method to the class so it can build the URL and
#         # we can assert things about the call that will be attempted to the
#         # internet
#         self.old_build_url = self.described_class._build_url
#         self.described_class._build_url = self.get_build_url_proxy()
#         self.instance = self.create_instance_of_described_class()
#         self.after_setup()

#     def tearDown(self):
#         """Reset attributes on items under test."""
#         self.described_class._build_url = self.old_build_url

#     def after_setup(self):
#         """No-op method to avoid people having to override setUp."""
#         pass


# class UnitIteratorHelper(UnitHelper):

#     """Base class for iterator based unit tests."""

#     def create_session_mock(self, *args):
#         """Override UnitHelper's create_session_mock method.

#         We want all methods to return an instance of the NullObject. This
#         class has a dummy ``__iter__`` implementation which we want for
#         methods that iterate over the results of a response.
#         """
#         # Retrieve a mocked session object
#         session = super(UnitIteratorHelper, self).create_mocked_session(*args)
#         # Initialize a NullObject which has magical properties
#         null = NullObject()
#         # Set it as the return value for every method
#         session.delete.return_value = null
#         session.get.return_value = null
#         session.patch.return_value = null
#         session.post.return_value = null
#         session.put.return_value = null
#         return session

#     def get_next(self, iterator):
#         """Nicely wrap up a call to the iterator."""
#         try:
#             next(iterator)
#         except StopIteration:
#             pass

#     def patch_get_json(self):
#         """Patch a UltronIterator's _get_json method."""
#         self.get_json_mock = mock.patch.object(
#             ultron8.structs.UltronIterator, "_get_json"
#         )
#         self.patched_get_json = self.get_json_mock.start()
#         self.patched_get_json.return_value = []

#     def setUp(self):
#         """Use UnitHelper's setUp but also patch _get_json."""
#         super(UnitIteratorHelper, self).setUp()
#         self.patch_get_json()

#     def tearDown(self):
#         """Stop mocking _get_json."""
#         super(UnitIteratorHelper, self).tearDown()
#         self.get_json_mock.stop()


# class UnitRequiresAuthenticationHelper(UnitHelper):

#     """Helper for unit tests that demonstrate authentication is required."""

#     def after_setup(self):
#         """Disable authentication on the session."""
#         self.session.auth = None
#         self.session.has_auth.return_value = False

#     def assert_requires_auth(self, func, *args, **kwargs):
#         """
#         Assert error is raised if function is called without
#         authentication.
#         """
#         with pytest.raises(ultron8.exceptions.AuthenticationFailed):
#             func(*args, **kwargs)


class UnitUltronObjectHelper(UnitHelper):
    """Base class for UltronObject unit tests."""

    pass


is_py3 = (3, 0) <= sys.version_info < (4, 0)


class NullObject(object):
    def __init__(self, initializer=None):
        self.__dict__["initializer"] = initializer

    def __int__(self):
        return 0

    def __bool__(self):
        return False

    __nonzero__ = __bool__

    def __str__(self):
        return ""

    def __unicode__(self):
        return "" if is_py3 else "".decode()

    def __repr__(self):
        return "<NullObject({0})>".format(repr(self.__getattribute__("initializer")))

    def __getitem__(self, index):
        return self

    def __setitem__(self, index, value):
        pass

    def __getattr__(self, attr):
        return self

    def __setattr__(self, attr, value):
        pass

    def __call__(self, *args, **kwargs):
        return self

    def __contains__(self, other):
        return False

    def __iter__(self):
        return iter([])

    def __next__(self):
        raise StopIteration

    next = __next__

    def is_null(self):
        return True


def patch_yaml_files(files_dict, endswith=True):
    """Patch yaml_load with a dictionary of yaml files."""
    # match using endswith, start search with longest string
    matchlist = sorted(list(files_dict.keys()), key=len) if endswith else []

    def mock_open_f(fname, **_):
        """Mock open() in the yaml module, used by yaml_load."""
        # Return the mocked file on full match
        if fname in files_dict:
            LOGGER.debug("patch_yaml_files match %s", fname)
            res = StringIO(files_dict[fname])
            setattr(res, "name", fname)
            return res

        # Match using endswith
        for ends in matchlist:
            if fname.endswith(ends):
                LOGGER.debug("patch_yaml_files end match %s: %s", ends, fname)
                res = StringIO(files_dict[ends])
                setattr(res, "name", fname)
                return res

        # Not found
        raise FileNotFoundError("File not found: {}".format(fname))

    return mock.patch.object(yaml, "open", mock_open_f, create=True)


if __name__ == "__main__":
    data_fixture = "standard_default_config"
    data = example_data_to_str(data_fixture)
    print(data)
