from rest_framework.mixins import DestroyModelMixin

from drf_rior.generics import RIORGenericViewSet
from drf_rior.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    ListModelMixin,
)


class ModelViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RIORGenericViewSet,
):
    pass
