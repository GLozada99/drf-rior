from drf_spectacular.openapi import AutoSchema

from drf_rior.generics import RIORGenericViewSet


class RequestResponseAutoSchema(AutoSchema):
    """
    AutoSchema that uses different request and response serializers for classes
    that extend from RWRRGenericViewSet.
    """

    def get_request_serializer(self):
        print(self.view)
        if isinstance(self.view, RIORGenericViewSet):
            print(111111111)
            return self.view.get_request_serializer()
        print(222222222)
        return self._get_serializer()

    def get_response_serializers(self):
        if isinstance(self.view, RIORGenericViewSet):
            return self.view.get_response_serializer()
        return self._get_serializer()
