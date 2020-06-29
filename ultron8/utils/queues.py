# st2common
import uuid


def get_queue_name(queue_name_base, queue_name_suffix, add_random_uuid_to_suffix=True):
    """
    Get a queue name based on base name and suffix. You can also specify if you need a random
    UUID at the end of the final name generated. Format returned is
    ``queue_name_base.queue_.queue_name_suffix-UUID``.

    :param queue_name_base:  Base name for the queue.
    :type queue_name_base: ``str``

    :param queue_name_suffix: Base string for the suffix.
    :type queue_name_suffix: ``str``

    :param add_random_uuid_to_suffix: A boolean to indicate a UUID suffix to be
                                      added to name or not.
    :type add_random_uuid_to_suffix: ``boolean``

    :rtype: ``str``
    """
    if not queue_name_base:
        raise ValueError("Queue name base cannot be empty.")

    if not queue_name_suffix:
        return queue_name_base

    queue_suffix = queue_name_suffix
    if add_random_uuid_to_suffix:
        # Pick last 10 digits of uuid. Arbitrary but unique enough. Long queue names
        # might cause issues in RabbitMQ.
        u_hex = uuid.uuid4().hex
        uuid_suffix = uuid.uuid4().hex[len(u_hex) - 10 :]
        queue_suffix = "%s-%s" % (queue_name_suffix, uuid_suffix)

    queue_name = "%s.%s" % (queue_name_base, queue_suffix)
    return queue_name
