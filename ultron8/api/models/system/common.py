# st2common

__all__ = [
    "InvalidReferenceError",
    "InvalidResourceReferenceError",
    "ResourceReference",
]

PACK_SEPARATOR = "."


class InvalidReferenceError(ValueError):
    def __init__(self, ref):
        message = "Invalid reference: %s" % (ref)
        self.ref = ref
        self.message = message
        super(InvalidReferenceError, self).__init__(message)


class InvalidResourceReferenceError(ValueError):
    def __init__(self, ref):
        message = "Invalid resource reference: %s" % (ref)
        self.ref = ref
        self.message = message
        super(InvalidResourceReferenceError, self).__init__(message)


class ResourceReference(object):
    """
    Class used for referring to resources which belong to a content pack.
    """

    def __init__(self, pack=None, name=None):
        self.pack = self.validate_pack_name(pack=pack)
        self.name = name

        self.ref = self.to_string_reference(pack=pack, name=name)

    @staticmethod
    def is_resource_reference(ref):
        """
        This method uses a very naive approach to determine if the provided
        string is a resource reference - it only checks if this string contains
        a separator.

        :rtype ref: ``str``
        """
        return PACK_SEPARATOR in ref

    @staticmethod
    def from_string_reference(ref):
        pack = ResourceReference.get_pack(ref)
        name = ResourceReference.get_name(ref)

        return ResourceReference(pack=pack, name=name)

    @staticmethod
    def to_string_reference(pack=None, name=None):
        if pack and name:
            pack = ResourceReference.validate_pack_name(pack=pack)
            return PACK_SEPARATOR.join([pack, name])
        else:
            raise ValueError(
                "Both pack and name needed for building ref. pack=%s, name=%s"
                % (pack, name)
            )

    @staticmethod
    def validate_pack_name(pack):
        if PACK_SEPARATOR in pack.name:
            raise ValueError('Pack name should not contain "%s"' % (PACK_SEPARATOR))

        return pack.name

    @staticmethod
    def get_pack(ref):
        try:
            return ref.split(PACK_SEPARATOR, 1)[0]
        except (IndexError, AttributeError):
            raise InvalidResourceReferenceError(ref=ref)

    @staticmethod
    def get_name(ref):
        try:
            return ref.split(PACK_SEPARATOR, 1)[1]
        except (IndexError, AttributeError):
            raise InvalidResourceReferenceError(ref=ref)

    def __repr__(self):
        return "<ResourceReference pack=%s,name=%s,ref=%s>" % (
            self.pack,
            self.name,
            self.ref,
        )
