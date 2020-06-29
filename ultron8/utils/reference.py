# st2common
from ultron8.exceptions import db
from ultron8.api.models.system.common import ResourceReference


def get_ref_from_model(model):
    if model is None:
        raise ValueError("Model has None value.")
    model_id = getattr(model, "id", None)
    if model_id is None:
        raise db.UltronDBObjectMalformedError("model %s must contain id." % str(model))
    reference = {"id": str(model_id), "name": getattr(model, "name", None)}
    return reference


def get_model_from_ref(db_api, reference):
    if reference is None:
        raise db.UltronDBObjectNotFoundError("No reference supplied.")
    model_id = reference.get("id", None)
    if model_id is not None:
        return db_api.get_by_id(model_id)
    model_name = reference.get("name", None)
    if model_name is None:
        raise db.UltronDBObjectNotFoundError("Both name and id are None.")
    return db_api.get_by_name(model_name)


def get_model_by_resource_ref(db_api, ref):
    """
    Retrieve a DB model based on the resource reference.

    :param db_api: Class of the object to retrieve.
    :type db_api: ``object``

    :param ref: Resource reference.
    :type ref: ``str``

    :return: Retrieved object.
    """
    ref_obj = ResourceReference.from_string_reference(ref=ref)
    result = db_api.query(name=ref_obj.name, pack=ref_obj.pack).first()
    return result


def get_resource_ref_from_model(model):
    """
    Return a ResourceReference given db_model.

    :param model: DB model that contains name and pack.
    :type model: ``object``

    :return: ResourceReference.
    """
    try:
        name = model.name
        pack = model.pack
    except AttributeError:
        raise Exception(
            "Cannot build ResourceReference for model: %s. Name or pack missing."
            % model
        )
    return ResourceReference(name=name, pack=pack)


def get_str_resource_ref_from_model(model):
    """
    Return a resource reference as string given db_model.

    :param model: DB model that contains name and pack.
    :type model: ``object``

    :return: String representation of ResourceReference.
    """
    return get_resource_ref_from_model(model).ref
