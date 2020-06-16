# from app.models.domain.rwmodel import RWModel
from ultron8.api.models.rwmodel import RWModel


class RWSchema(RWModel):
    class Config(RWModel.Config):
        # NOTE: https://pydantic-docs.helpmanual.io/usage/model_config/
        # whether to allow usage of ORM mode
        # https://pydantic-docs.helpmanual.io/usage/models/#orm-mode-aka-arbitrary-class-instances
        # Pydantic models can be created from arbitrary class instances to support models that map to ORM objects.
        orm_mode = True
