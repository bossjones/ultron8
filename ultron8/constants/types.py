# st2common
from enum import Enum

__all__ = ["ResourceType"]


class ResourceType(str, Enum):
    """
    Enum representing a valid resource type in a system.
    """

    # System resources
    RUNNER_TYPE = "runner_type"

    # Pack resources
    PACK = "pack"
    ACTION = "action"
    ACTION_ALIAS = "action_alias"
    SENSOR_TYPE = "sensor_type"
    TRIGGER_TYPE = "trigger_type"
    TRIGGER = "trigger"
    TRIGGER_INSTANCE = "trigger_instance"
    RULE = "rule"
    RULE_ENFORCEMENT = "rule_enforcement"

    # Note: Policy type is a global resource and policy belong to a pack
    POLICY_TYPE = "policy_type"
    POLICY = "policy"

    # Other resources
    EXECUTION = "execution"
    EXECUTION_REQUEST = "execution_request"
    KEY_VALUE_PAIR = "key_value_pair"

    WEBHOOK = "webhook"
    TIMER = "timer"
    API_KEY = "api_key"
    TRACE = "trace"
    TIMER = "timer"

    # Special resource type for stream related stuff
    STREAM = "stream"

    INQUIRY = "inquiry"

    UNKNOWN = "unknown"
