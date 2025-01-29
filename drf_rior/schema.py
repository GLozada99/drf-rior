from drf_spectacular.openapi import AutoSchema

from drf_rior.generics import GenericViewSet


class RequestResponseAutoSchema(AutoSchema):
    """
    AutoSchema that uses different request and response serializers for classes
    that extend from drf_rior.generics.GenericViewSet.
    """

    def get_request_serializer(self):
        if isinstance(self.view, GenericViewSet):
            return self.view.get_request_serializer()
        return self._get_serializer()

    def get_response_serializers(self):
        if isinstance(self.view, GenericViewSet):
            return self.view.get_response_serializer()
        return self._get_serializer()
