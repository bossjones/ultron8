# SOURCE: https://blog.bartab.fr/fastapi-logging-on-the-fly/
import logging
from fastapi import APIRouter
from fastapi import HTTPException
from ultron8.api.models.log import LoggerModel, LoggerPatch

LOG_LEVELS = {
    "critical": logging.CRITICAL,
    "error": logging.ERROR,
    "warning": logging.WARNING,
    "info": logging.INFO,
    "debug": logging.DEBUG,
}

LOGGER = logging.getLogger(__name__)

router = APIRouter()


def get_lm_from_tree(loggertree: LoggerModel, find_me: str) -> LoggerModel:
    if find_me == loggertree.name:
        LOGGER.debug("Found")
        return loggertree
    else:
        for ch in loggertree.children:
            LOGGER.debug(f"Looking in: {ch.name}")
            i = get_lm_from_tree(ch, find_me)
            if i:
                return i


def generate_tree() -> LoggerModel:
    # adapted from logging_tree package https://github.com/brandon-rhodes/logging_tree
    rootm = LoggerModel(
        name="root", level=logging.getLogger().getEffectiveLevel(), children=[]
    )
    nodesm = {}
    items = list(logging.root.manager.loggerDict.items())  # type: ignore
    items.sort()
    for name, loggeritem in items:
        if isinstance(loggeritem, logging.PlaceHolder):
            nodesm[name] = nodem = LoggerModel(name=name, children=[])
        else:
            nodesm[name] = nodem = LoggerModel(
                name=name, level=loggeritem.getEffectiveLevel(), children=[]
            )
        i = name.rfind(".", 0, len(name) - 1)  # same formula used in `logging`
        if i == -1:
            parentm = rootm
        else:
            parentm = nodesm[name[:i]]
        parentm.children.append(nodem)
    return rootm


@router.get("/{logger_name}", response_model=LoggerModel)
def logger_get(logger_name: str):
    LOGGER.debug(f"getting logger {logger_name}")
    rootm = generate_tree()
    lm = get_lm_from_tree(rootm, logger_name)
    if lm is None:
        raise HTTPException(status_code=404, detail=f"Logger {logger_name} not found")
    return lm


@router.patch("/")
def logger_patch(loggerpatch: LoggerPatch):
    rootm = generate_tree()
    lm = get_lm_from_tree(rootm, loggerpatch.name)
    LOGGER.debug(f"Actual level of {lm.name} is {lm.level}")
    LOGGER.debug(f"Setting {loggerpatch.name} to {loggerpatch.level}")
    logging.getLogger(loggerpatch.name).setLevel(LOG_LEVELS[loggerpatch.level])
    return loggerpatch


@router.get("/", response_model=LoggerModel)
def loggers_list():
    rootm = generate_tree()
    LOGGER.debug(rootm)
    return rootm
