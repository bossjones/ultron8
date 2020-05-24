from fastapi.encoders import jsonable_encoder


def orm_to_model(orm_obj, model_obj):
    orm_data = jsonable_encoder(orm_obj)
    update_data = model_obj.dict(exclude_unset=True)
    for field in orm_data:
        if field in update_data:
            setattr(orm_obj, field, update_data[field])

    return orm_obj
