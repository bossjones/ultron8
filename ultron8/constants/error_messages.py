# st2common

__all__ = ["PACK_VIRTUALENV_DOESNT_EXIST", "PACK_VIRTUALENV_USES_PYTHON3"]

PACK_VIRTUALENV_DOESNT_EXIST = """
The virtual environment (%(virtualenv_path)s) for pack "%(pack)s" does not exist. Normally this is
created when you install a pack using "st2 pack install". If you installed your pack by some other
means, you can create a new virtual environment using the command:
"st2 run packs.setup_virtualenv packs=%(pack)s"
"""

PACK_VIRTUALENV_USES_PYTHON3 = """
Virtual environment (%(virtualenv_path)s) for pack "%(pack)s" is using Python 3.
Using Python 3 virtual environments in mixed deployments is only supported for Python runner
actions and not sensors. If you want to run this sensor, please re-recreate the
virtual environment with python2 binary:
"st2 run packs.setup_virtualenv packs=%(pack)s python3=false"
"""
