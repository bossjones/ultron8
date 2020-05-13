# """Test Constants for trigger."""
# # pylint: disable=protected-access
# import logging
# import pytest
# import ultron8
# from ultron8.constants import trigger
# from ultron8.constants.packs import SYSTEM_PACK_NAME
# from ultron8.api.models.system.common import ResourceReference

# logger = logging.getLogger(__name__)

# @pytest.mark.constantsonly
# @pytest.mark.unittest
# class TestConstantsTrigger(object):
#     def test_constant_trigger(self):
#         assert trigger.ACTION_SENSOR_TRIGGER == {
#             "name": "ultron8.generic.actiontrigger",
#             "packs_name": SYSTEM_PACK_NAME,
#             "description": "Trigger encapsulating the completion of an action execution.",
#             "payload_schema": {
#                 "type": "object",
#                 "properties": {
#                     "execution_id": {},
#                     "status": {},
#                     "start_timestamp": {},
#                     "action_name": {},
#                     "action_ref": {},
#                     "runner_ref": {},
#                     "parameters": {},
#                     "result": {},
#                 },
#             },
#         }


#         assert trigger.ACTION_FILE_WRITTEN_TRIGGER == {
#             "name": "ultron8.action.file_writen",
#             "packs_name": SYSTEM_PACK_NAME,
#             "description": "Trigger encapsulating action file being written on disk.",
#             "payload_schema": {
#                 "type": "object",
#                 "properties": {"ref": {}, "file_path": {}, "host_info": {}},
#             },
#         }
#         assert trigger.NOTIFY_TRIGGER == {
#             "name": "ultron8.generic.notifytrigger",
#             "packs_name": SYSTEM_PACK_NAME,
#             "description": "Notification trigger.",
#             "payload_schema": {
#                 "type": "object",
#                 "properties": {
#                     "execution_id": {},
#                     "status": {},
#                     "start_timestamp": {},
#                     "end_timestamp": {},
#                     "action_ref": {},
#                     "runner_ref": {},
#                     "channel": {},
#                     "route": {},
#                     "message": {},
#                     "data": {},
#                 },
#             },
#         }
#         assert trigger.INQUIRY_TRIGGER  == {
#             "name": "ultron8.generic.inquiry",
#             "packs_name": SYSTEM_PACK_NAME,
#             "description": 'Trigger indicating a new "inquiry" has entered "pending" status',
#             "payload_schema": {
#                 "type": "object",
#                 "properties": {
#                     "id": {
#                         "type": "string",
#                         "description": "ID of the new inquiry.",
#                         "required": True,
#                     },
#                     "route": {
#                         "type": "string",
#                         "description": "An arbitrary value for allowing rules "
#                         "to route to proper notification channel.",
#                         "required": True,
#                     },
#                 },
#                 "additionalProperties": False,
#             },
#         }
#         assert trigger.SENSOR_SPAWN_TRIGGER  == {
#             "name": "ultron8.sensor.process_spawn",
#             "packs_name": SYSTEM_PACK_NAME,
#             "description": "Trigger indicating sensor process is started up.",
#             "payload_schema": {"type": "object", "properties": {"object": {}}},
#         }
#         # assert trigger.SENSOR_EXIT_TRIGGER  ==
#         # assert trigger.KEY_VALUE_PAIR_CREATE_TRIGGER  ==
#         # assert trigger.KEY_VALUE_PAIR_UPDATE_TRIGGER  ==
#         # assert trigger.KEY_VALUE_PAIR_VALUE_CHANGE_TRIGGER  ==
#         # assert trigger.INTERNAL_TRIGGER_TYPES  ==
#         # assert trigger.WEBHOOKS_PARAMETERS_SCHEMA  ==
#         # assert trigger.WEBHOOK_TRIGGER_TYPES  ==
#         # assert trigger.WEBHOOK_TRIGGER_TYPE  ==
#         # assert trigger.INTERVAL_PARAMETERS_SCHEMA  ==
#         # assert trigger.DATE_PARAMETERS_SCHEMA  ==
#         # assert trigger.TIMER_PAYLOAD_SCHEMA  ==
#         # assert trigger.INTERVAL_TIMER_TRIGGER_REF  ==
#         # assert trigger.DATE_TIMER_TRIGGER_REF  ==
#         # assert trigger.CRON_TIMER_TRIGGER_REF  ==
#         # assert trigger.TIMER_TRIGGER_TYPES  ==
#         # assert trigger.SYSTEM_TRIGGER_TYPES  ==
#         # assert trigger.TRIGGER_INSTANCE_STATUSES  ==
