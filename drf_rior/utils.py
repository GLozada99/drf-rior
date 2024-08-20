import dataclasses
from typing import Type, Optional

from rest_framework import serializers

SerializerType = Type[serializers.Serializer]
OptionalSerializerType = Optional[SerializerType]


@dataclasses.dataclass
class SerializerActionViewGroup:
    """
    Used to define the serializers to be used in any action from a view that extends
    from RWRRGenericAPIView
    """

    default: SerializerType
    request: OptionalSerializerType = None
    input: OptionalSerializerType = None
    output: OptionalSerializerType = None
    response: OptionalSerializerType = None
