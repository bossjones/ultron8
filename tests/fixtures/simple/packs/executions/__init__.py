from __future__ import absolute_import
import os
import glob
import yaml
import six


PATH = os.path.dirname(os.path.realpath(__file__))
FILES = glob.glob("%s/*.yaml" % PATH)
ARTIFACTS = {}


for f in FILES:
    f_name = os.path.split(f)[1]
    name = six.text_type(os.path.splitext(f_name)[0])
    with open(f, "r") as fd:
        ARTIFACTS[name] = yaml.safe_load(fd)
    if isinstance(ARTIFACTS[name], dict):
        print("we have a dict")
        # ARTIFACTS[name][u'id'] = int(ARTIFACTS[name][u'id'])
    elif isinstance(ARTIFACTS[name], list):
        print("we have a list")
        # for item in ARTIFACTS[name]:
        #     item[u'id'] = int(item[u'id'])


# smoke tests
if __name__ == "__main__":
    from tests.fixtures.simple.packs import executions as fixture
    import pprint

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(fixture)
