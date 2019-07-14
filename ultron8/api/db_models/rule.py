from sqlalchemy import and_
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Unicode
from sqlalchemy import UnicodeText
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.sql import func

from ultron8.api.db.u_sqlite.base_class import Base
from ultron8.api.db_models.utils import ProxiedDictMixin


class RuleTypeParameter(Base):
    """A parameter about a rule type."""

    __tablename__ = "rule_type_parameter"

    rule_id = Column("rule_id", Integer, ForeignKey("rule_type.id"), primary_key=True)
    key = Column("key", Unicode(64), primary_key=True)
    value = Column("value", UnicodeText)


class RuleType(ProxiedDictMixin, Base):
    """A rule type."""

    __tablename__ = "rule_type"
    id = Column("id", Integer, primary_key=True, index=True)
    name = Column("name", Unicode(100))
    ref_key = Column("ref_key", String(255))
    ref_value = Column("ref_value", String(255))
    # parameters = dictonary of RuleTypeParameter, w/ key,val
    parameters = relationship(
        "RuleTypeParameter", collection_class=attribute_mapped_collection("key")
    )

    # -------------------------------------------------------------------------
    # SOURCE: https://docs.sqlalchemy.org/en/13/orm/examples.html#module-examples.vertical
    # SOURCE: https://docs.sqlalchemy.org/en/13/_modules/examples/vertical/dictlike.html
    # Vertical Attribute Mapping
    # Illustrates "vertical table" mappings.

    # A "vertical table" refers to a technique where individual attributes of an object are stored as distinct rows in a table. The "vertical table" technique is used to persist objects which can have a varied set of attributes, at the expense of simple query control and brevity. It is commonly found in content/document management systems in order to represent user-created structures flexibly.

    # Two variants on the approach are given. In the second, each row references a "datatype" which contains information about the type of information stored in the attribute, such as integer, string, or date.
    # -------------------------------------------------------------------------
    _proxied = association_proxy(
        "parameters",
        "value",
        creator=lambda key, value: RuleTypeParameter(key=key, value=value),
    )

    def __init__(self, name, *args, **values):
        super(RuleType, self).__init__(*args, **values)
        self.name = name

    def __repr__(self):
        return "RuleType(%r)" % self.name

    @classmethod
    def with_characteristic(self, key, value):
        return self.parameters.any(key=key, value=value)


class Rules(ProxiedDictMixin, Base):
    """Db Schema for Rules table. Specifies the action to invoke on the occurrence of a Trigger. It
    also includes the transformation to perform to match the impedance
    between the payload of a TriggerInstance and input of a action.
    Attribute:
        trigger: Trigger that trips this rule.
        criteria:
        action: Action to execute when the rule is tripped.
        status: enabled or disabled. If disabled occurrence of the trigger
        does not lead to execution of a action and vice-versa.
    """

    __tablename__ = "rules"

    id = Column("id", Integer, primary_key=True, index=True)
    # trigger_type = Column(String(255))
    name = Column("name", String(255))
    pack = Column("pack", String(255))
    description = Column("description", String(255))
    enabled = Column("enabled", Boolean)
    trigger = Column("trigger", String(255))
    action = Column("action", String(255))
    ref = Column("ref", String(255))
    type = Column("type", String(255))
    # type = relationship(
    #     "RuleType", collection_class=attribute_mapped_collection("ref_key")
    # )
    # _proxied = association_proxy(
    #     "type",
    #     "ref_value",
    #     creator=lambda key, value: RuleType(key=key, value=value),
    # )
    criteria = Column("criteria", String(255))
    context = Column("context", String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.utcnow())
    updated_at = Column(DateTime(timezone=True), onupdate=func.utcnow())


# if "__main__" == __name__:
#     rules = Rules()

#     print(rules)

# if __name__ == "__main__":
#     engine = create_engine("sqlite://")
#     Base.metadata.create_all(engine)

#     session = Session(engine)

#     # create catalog
#     tshirt, mug, hat, crowbar = (
#         Item("SA T-Shirt", 10.99),
#         Item("SA Mug", 6.50),
#         Item("SA Hat", 8.99),
#         Item("MySQL Crowbar", 16.99),
#     )
#     session.add_all([tshirt, mug, hat, crowbar])
#     session.commit()

#     # create an order
#     order = Order("john smith")

#     # add three OrderItem associations to the Order and save
#     order.order_items.append(OrderItem(mug))
#     order.order_items.append(OrderItem(crowbar, 10.99))
#     order.order_items.append(OrderItem(hat))
#     session.add(order)
#     session.commit()

#     # query the order, print items
#     order = session.query(Order).filter_by(customer_name="john smith").one()
#     print(
#         [
#             (order_item.item.description, order_item.price)
#             for order_item in order.order_items
#         ]
#     )

#     # print customers who bought 'MySQL Crowbar' on sale
#     q = session.query(Order).join("order_items", "item")
#     q = q.filter(
#         and_(Item.description == "MySQL Crowbar", Item.price > OrderItem.price)
#     )

#     print([order.customer_name for order in q])
