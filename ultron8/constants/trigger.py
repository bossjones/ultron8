from ultron8.api.models.system.common import ResourceReference
from ultron8.constants.packs import SYSTEM_PACK_NAME

__all__ = [
    "WEBHOOKS_PARAMETERS_SCHEMA",
    "WEBHOOKS_PAYLOAD_SCHEMA",
    "INTERVAL_PARAMETERS_SCHEMA",
    "DATE_PARAMETERS_SCHEMA",
    "CRON_PARAMETERS_SCHEMA",
    "TIMER_PAYLOAD_SCHEMA",
    "ACTION_SENSOR_TRIGGER",
    "NOTIFY_TRIGGER",
    "ACTION_FILE_WRITTEN_TRIGGER",
    "INQUIRY_TRIGGER",
    "TIMER_TRIGGER_TYPES",
    "WEBHOOK_TRIGGER_TYPES",
    "WEBHOOK_TRIGGER_TYPE",
    "INTERNAL_TRIGGER_TYPES",
    "SYSTEM_TRIGGER_TYPES",
    "INTERVAL_TIMER_TRIGGER_REF",
    "DATE_TIMER_TRIGGER_REF",
    "CRON_TIMER_TRIGGER_REF",
    "TRIGGER_INSTANCE_STATUSES",
    "TRIGGER_INSTANCE_PENDING",
    "TRIGGER_INSTANCE_PROCESSING",
    "TRIGGER_INSTANCE_PROCESSED",
    "TRIGGER_INSTANCE_PROCESSING_FAILED",
]

# Action resource triggers
ACTION_SENSOR_TRIGGER = {
    "name": "ultron8.generic.actiontrigger",
    "packs_name": SYSTEM_PACK_NAME,
    "description": "Trigger encapsulating the completion of an action execution.",
    "payload_schema": {
        "type": "object",
        "properties": {
            "execution_id": {},
            "status": {},
            "start_timestamp": {},
            "action_name": {},
            "action_ref": {},
            "runner_ref": {},
            "parameters": {},
            "result": {},
        },
    },
}

ACTION_FILE_WRITTEN_TRIGGER = {
    "name": "ultron8.action.file_writen",
    "packs_name": SYSTEM_PACK_NAME,
    "description": "Trigger encapsulating action file being written on disk.",
    "payload_schema": {
        "type": "object",
        "properties": {"ref": {}, "file_path": {}, "host_info": {}},
    },
}

NOTIFY_TRIGGER = {
    "name": "ultron8.generic.notifytrigger",
    "packs_name": SYSTEM_PACK_NAME,
    "description": "Notification trigger.",
    "payload_schema": {
        "type": "object",
        "properties": {
            "execution_id": {},
            "status": {},
            "start_timestamp": {},
            "end_timestamp": {},
            "action_ref": {},
            "runner_ref": {},
            "channel": {},
            "route": {},
            "message": {},
            "data": {},
        },
    },
}

INQUIRY_TRIGGER = {
    "name": "ultron8.generic.inquiry",
    "packs_name": SYSTEM_PACK_NAME,
    "description": 'Trigger indicating a new "inquiry" has entered "pending" status',
    "payload_schema": {
        "type": "object",
        "properties": {
            "id": {
                "type": "string",
                "description": "ID of the new inquiry.",
                "required": True,
            },
            "route": {
                "type": "string",
                "description": "An arbitrary value for allowing rules "
                "to route to proper notification channel.",
                "required": True,
            },
        },
        "additionalProperties": False,
    },
}

# Sensor spawn/exit triggers.
SENSOR_SPAWN_TRIGGER = {
    "name": "ultron8.sensor.process_spawn",
    "packs_name": SYSTEM_PACK_NAME,
    "description": "Trigger indicating sensor process is started up.",
    "payload_schema": {"type": "object", "properties": {"object": {}}},
}

SENSOR_EXIT_TRIGGER = {
    "name": "ultron8.sensor.process_exit",
    "packs_name": SYSTEM_PACK_NAME,
    "description": "Trigger indicating sensor process is stopped.",
    "payload_schema": {"type": "object", "properties": {"object": {}}},
}

# KeyValuePair resource triggers
KEY_VALUE_PAIR_CREATE_TRIGGER = {
    "name": "ultron8.key_value_pair.create",
    "packs_name": SYSTEM_PACK_NAME,
    "description": "Trigger encapsulating datastore item creation.",
    "payload_schema": {"type": "object", "properties": {"object": {}}},
}

KEY_VALUE_PAIR_UPDATE_TRIGGER = {
    "name": "ultron8.key_value_pair.update",
    "packs_name": SYSTEM_PACK_NAME,
    "description": "Trigger encapsulating datastore set action.",
    "payload_schema": {"type": "object", "properties": {"object": {}}},
}

KEY_VALUE_PAIR_VALUE_CHANGE_TRIGGER = {
    "name": "ultron8.key_value_pair.value_change",
    "packs_name": SYSTEM_PACK_NAME,
    "description": "Trigger encapsulating a change of datastore item value.",
    "payload_schema": {
        "type": "object",
        "properties": {"old_object": {}, "new_object": {}},
    },
}

KEY_VALUE_PAIR_DELETE_TRIGGER = {
    "name": "ultron8.key_value_pair.delete",
    "packs_name": SYSTEM_PACK_NAME,
    "description": "Trigger encapsulating datastore item deletion.",
    "payload_schema": {"type": "object", "properties": {"object": {}}},
}

# Internal system triggers which are available for each resource
INTERNAL_TRIGGER_TYPES = {
    "action": [
        ACTION_SENSOR_TRIGGER,
        NOTIFY_TRIGGER,
        ACTION_FILE_WRITTEN_TRIGGER,
        INQUIRY_TRIGGER,
    ],
    "sensor": [SENSOR_SPAWN_TRIGGER, SENSOR_EXIT_TRIGGER],
    "key_value_pair": [
        KEY_VALUE_PAIR_CREATE_TRIGGER,
        KEY_VALUE_PAIR_UPDATE_TRIGGER,
        KEY_VALUE_PAIR_VALUE_CHANGE_TRIGGER,
        KEY_VALUE_PAIR_DELETE_TRIGGER,
    ],
}


WEBHOOKS_PARAMETERS_SCHEMA = {
    "type": "object",
    "properties": {"url": {"type": "string", "required": True}},
    "additionalProperties": False,
}


WEBHOOKS_PAYLOAD_SCHEMA = {
    "type": "object",
    "properties": {
        "headers": {"type": "object"},
        "body": {"anyOf": [{"type": "array"}, {"type": "object"}]},
    },
}

WEBHOOK_TRIGGER_TYPES = {
    ResourceReference.to_string_reference(SYSTEM_PACK_NAME, "ultron8.webhook"): {
        "name": "ultron8.webhook",
        "packs_name": SYSTEM_PACK_NAME,
        "description": (
            "Trigger type for registering webhooks that can consume"
            " arbitrary payload."
        ),
        "parameters_schema": WEBHOOKS_PARAMETERS_SCHEMA,
        "payload_schema": WEBHOOKS_PAYLOAD_SCHEMA,
    }
}
WEBHOOK_TRIGGER_TYPE = list(WEBHOOK_TRIGGER_TYPES.keys())[0]

# Timer specs

INTERVAL_PARAMETERS_SCHEMA = {
    "type": "object",
    "properties": {
        "timezone": {"type": "string"},
        "unit": {
            "enum": ["weeks", "days", "hours", "minutes", "seconds"],
            "required": True,
        },
        "delta": {"type": "integer", "required": True},
    },
    "additionalProperties": False,
}

DATE_PARAMETERS_SCHEMA = {
    "type": "object",
    "properties": {
        "timezone": {"type": "string"},
        "date": {"type": "string", "format": "date-time", "required": True},
    },
    "additionalProperties": False,
}

CRON_PARAMETERS_SCHEMA = {
    "type": "object",
    "properties": {
        "timezone": {"type": "string"},
        "year": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
        "month": {
            "anyOf": [{"type": "string"}, {"type": "integer"}],
            "minimum": 1,
            "maximum": 12,
        },
        "day": {
            "anyOf": [{"type": "string"}, {"type": "integer"}],
            "minimum": 1,
            "maximum": 31,
        },
        "week": {
            "anyOf": [{"type": "string"}, {"type": "integer"}],
            "minimum": 1,
            "maximum": 53,
        },
        "day_of_week": {
            "anyOf": [{"type": "string"}, {"type": "integer"}],
            "minimum": 0,
            "maximum": 6,
        },
        "hour": {
            "anyOf": [{"type": "string"}, {"type": "integer"}],
            "minimum": 0,
            "maximum": 23,
        },
        "minute": {
            "anyOf": [{"type": "string"}, {"type": "integer"}],
            "minimum": 0,
            "maximum": 59,
        },
        "second": {
            "anyOf": [{"type": "string"}, {"type": "integer"}],
            "minimum": 0,
            "maximum": 59,
        },
    },
    "additionalProperties": False,
}

TIMER_PAYLOAD_SCHEMA = {
    "type": "object",
    "properties": {
        "executed_at": {
            "type": "string",
            "format": "date-time",
            "default": "2014-07-30 05:04:24.578325",
        },
        "schedule": {"type": "object", "default": {"delta": 30, "units": "seconds"}},
    },
}

INTERVAL_TIMER_TRIGGER_REF = ResourceReference.to_string_reference(
    SYSTEM_PACK_NAME, "ultron8.IntervalTimer"
)
DATE_TIMER_TRIGGER_REF = ResourceReference.to_string_reference(
    SYSTEM_PACK_NAME, "ultron8.DateTimer"
)
CRON_TIMER_TRIGGER_REF = ResourceReference.to_string_reference(
    SYSTEM_PACK_NAME, "ultron8.CronTimer"
)

TIMER_TRIGGER_TYPES = {
    INTERVAL_TIMER_TRIGGER_REF: {
        "name": "ultron8.IntervalTimer",
        "packs_name": SYSTEM_PACK_NAME,
        "description": "Triggers on specified intervals. e.g. every 30s, 1week etc.",
        "payload_schema": TIMER_PAYLOAD_SCHEMA,
        "parameters_schema": INTERVAL_PARAMETERS_SCHEMA,
    },
    DATE_TIMER_TRIGGER_REF: {
        "name": "ultron8.DateTimer",
        "packs_name": SYSTEM_PACK_NAME,
        "description": "Triggers exactly once when the current time matches the specified time. "
        "e.g. timezone:UTC date:2014-12-31 23:59:59.",
        "payload_schema": TIMER_PAYLOAD_SCHEMA,
        "parameters_schema": DATE_PARAMETERS_SCHEMA,
    },
    CRON_TIMER_TRIGGER_REF: {
        "name": "ultron8.CronTimer",
        "packs_name": SYSTEM_PACK_NAME,
        "description": "Triggers whenever current time matches the specified time constaints like "
        "a UNIX cron scheduler.",
        "payload_schema": TIMER_PAYLOAD_SCHEMA,
        "parameters_schema": CRON_PARAMETERS_SCHEMA,
    },
}

SYSTEM_TRIGGER_TYPES = dict(
    list(WEBHOOK_TRIGGER_TYPES.items()) + list(TIMER_TRIGGER_TYPES.items())
)

# various status to record lifecycle of a TriggerInstance
TRIGGER_INSTANCE_PENDING = "pending"
TRIGGER_INSTANCE_PROCESSING = "processing"
TRIGGER_INSTANCE_PROCESSED = "processed"
TRIGGER_INSTANCE_PROCESSING_FAILED = "processing_failed"


TRIGGER_INSTANCE_STATUSES = [
    TRIGGER_INSTANCE_PENDING,
    TRIGGER_INSTANCE_PROCESSING,
    TRIGGER_INSTANCE_PROCESSED,
    TRIGGER_INSTANCE_PROCESSING_FAILED,
]
