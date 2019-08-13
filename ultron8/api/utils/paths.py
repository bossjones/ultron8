# Inspiration: https://github.com/3lpsy/bountydns/blob/master/bountydns/core/utils/paths.py

from os.path import abspath, dirname, join

_utils_dir = abspath(dirname(__file__))


def _ajoin(target, path):
    return abspath(join(target, path))


def core_dir(path=None):
    if not path:
        return _ajoin(_utils_dir, "..")
    return _ajoin(core_dir(), path)


# def project_dir(path=None):
#     if not path:
#         return _ajoin(core_dir(), "..")
#     return _ajoin(project_dir(), path)


def crud_dir(path=None):
    if not path:
        return _ajoin(_utils_dir, "..")
    return _ajoin(crud_dir(), path)


def db_dir(path=None):
    if not path:
        return _ajoin(_utils_dir, "..")
    return _ajoin(db_dir(), path)


def db_models_dir(path=None):
    if not path:
        return _ajoin(_utils_dir, "..")
    return _ajoin(db_models_dir(), path)


def models_dir(path=None):
    if not path:
        return _ajoin(_utils_dir(), "..")
    return _ajoin(models_dir(), path)


def routers_dir(path=None):
    if not path:
        return _ajoin(_utils_dir(), "..")
    return _ajoin(routers_dir(), path)


# def templates_dir(path=None):
#     if not path:
#         return _ajoin(_utils_dir(), "..")
#     return _ajoin(project_dir(), path)

# def views_dir(path=None):
#     if not path:
#         return _ajoin(_utils_dir(), "..")
#     return _ajoin(views_dir(), path)


# ultron8/api/utils
# def api_dir(path=None):
#     if not path:
#         return _ajoin(core_dir(), "..")
#     return _ajoin(api_dir(), path)

# def storage_dir(path=None):
#     if not path:
#         return project_dir("storage")
#     return _ajoin(storage_dir(), path)

# def root_dir(path=None):
#     if not path:
#         return _ajoin(project_dir(), "..")
#     return _ajoin(root_dir(), path)


# def cli_dir(path=None):
#     if not path:
#         return project_dir("cli")
#     return _ajoin(cli_dir(), path)


# def dns_dir(path=None):
#     if not path:
#         return project_dir("dns")
#     return _ajoin(dns_dir(), path)


# def api_dir(path=None):
#     if not path:
#         return project_dir("api")
#     return _ajoin(api_dir(), path)


# def db_dir(path=None):
#     if not path:
#         return project_dir("db")
#     return _ajoin(db_dir(), path)


# def webui_dir(path=None):
#     if not path:
#         return root_dir("webui")
#     return _ajoin(webui_dir(), path)


# def landing_dir(path=None):
#     if not path:
#         return root_dir("landing")
#     return _ajoin(landing_dir(), path)


# def test_dir(path=None):
#     if not path:
#         return project_dir("tests")
#     return _ajoin(test_dir(), path)


# def env_dir(path=None):
#     if not path:
#         return root_dir(".env")
#     return _ajoin(env_dir(), path)
