# import json
# import yaml

# from st2common.constants.keyvalue import FULL_SYSTEM_SCOPE
# from ultron8.utils import jinja as jinja_utils
# from st2common.services.keyvalues import KeyValueLookup


# class JinjaUtilsDataFilterTestCase:

#     def test_filter_from_json_string(self):
#         env = jinja_utils.get_jinja_environment()
#         expected_obj = {'a': 'b', 'c': {'d': 'e', 'f': 1, 'g': True}}
#         obj_json_str = '{"a": "b", "c": {"d": "e", "f": 1, "g": true}}'

#         template = '{{k1 | from_json_string}}'

#         obj_str = env.from_string(template).render({'k1': obj_json_str})
#         obj = eval(obj_str)
#         assert obj == expected_obj

#         # With KeyValueLookup object
#         env = jinja_utils.get_jinja_environment()
#         obj_json_str = '["a", "b", "c"]'
#         expected_obj = ['a', 'b', 'c']

#         template = '{{ k1 | from_json_string}}'

#         lookup = KeyValueLookup(scope=FULL_SYSTEM_SCOPE, key_prefix='a')
#         lookup._value_cache['a'] = obj_json_str
#         obj_str = env.from_string(template).render({'k1': lookup})
#         obj = eval(obj_str)
#         assert obj == expected_obj

#     def test_filter_from_yaml_string(self):
#         env = jinja_utils.get_jinja_environment()
#         expected_obj = {'a': 'b', 'c': {'d': 'e', 'f': 1, 'g': True}}
#         obj_yaml_str = ("---\n"
#                         "a: b\n"
#                         "c:\n"
#                         "  d: e\n"
#                         "  f: 1\n"
#                         "  g: true\n")

#         template = '{{k1 | from_yaml_string}}'
#         obj_str = env.from_string(template).render({'k1': obj_yaml_str})
#         obj = eval(obj_str)
#         assert obj == expected_obj

#         # With KeyValueLookup object
#         env = jinja_utils.get_jinja_environment()
#         obj_yaml_str = ("---\n"
#                         "- a\n"
#                         "- b\n"
#                         "- c\n")
#         expected_obj = ['a', 'b', 'c']

#         template = '{{ k1 | from_yaml_string }}'

#         lookup = KeyValueLookup(scope=FULL_SYSTEM_SCOPE, key_prefix='b')
#         lookup._value_cache['b'] = obj_yaml_str
#         obj_str = env.from_string(template).render({'k1': lookup})
#         obj = eval(obj_str)
#         assert obj == expected_obj

#     def test_filter_to_json_string(self):
#         env = jinja_utils.get_jinja_environment()
#         obj = {'a': 'b', 'c': {'d': 'e', 'f': 1, 'g': True}}

#         template = '{{k1 | to_json_string}}'

#         obj_json_str = env.from_string(template).render({'k1': obj})
#         actual_obj = json.loads(obj_json_str)
#         assert obj == actual_obj

#     def test_filter_to_yaml_string(self):
#         env = jinja_utils.get_jinja_environment()
#         obj = {'a': 'b', 'c': {'d': 'e', 'f': 1, 'g': True}}

#         template = '{{k1 | to_yaml_string}}'
#         obj_yaml_str = env.from_string(template).render({'k1': obj})
#         actual_obj = yaml.safe_load(obj_yaml_str)
#         assert obj == actual_obj
