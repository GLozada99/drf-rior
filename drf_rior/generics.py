from typing import Optional, Type

from rest_framework import serializers, viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response

from drf_rior.exceptions import ClassDefinitionError
from drf_rior.utils import SerializerActionViewGroup


class RIORGenericViewSet(viewsets.GenericViewSet):
    """
    ViewSet that allows for setting values for serializers for the following:
    - request
    - input
    - output
    - response
    - default
    It uses the SerializerActionViewGroup
    The `request` is used for the Request OpenAPI schema. Represents the data
    received from the client.
    The `input` is used to serialize the input data into the object related to that
    view.
    The `output` is used to serialize the output object into primitive data.
    The `response` is used for the OpenAPI schema. Represents the data that the
    client will receive.
    The `default` will be used in all previous occurrences if they were not
    specifically defined.

    The order of processing is:
    `request` -> `input` -> `output` -> `response`
    """

    action_serializer_group: dict[str, SerializerActionViewGroup]

    def __init__(self, **kwargs):
        if getattr(self, "action_serializer_group", None) is None:
            raise ClassDefinitionError("action_serializer_group must be declared.")

        if not isinstance(self.action_serializer_group, dict):
            raise ClassDefinitionError("action_serializer_group must be a dict.")

        if not self.serializer_class:
            raise ClassDefinitionError("serializer_class must be declared.")

        super().__init__(**kwargs)

    def get_group(self) -> Optional[SerializerActionViewGroup]:
        """
        Gets the `SerializerActionViewGroup` based on the current action of
        the view.
        :return: `SerializerActionViewGroup` instance that handles the current action of the view
        """
        return self.action_serializer_group.get(self.action)

    def _get_serializer_class(
        self, serializer_type: str
    ) -> Type[serializers.Serializer]:
        """
        Gets the serializer class to be used based on the group for the action,
        and the provided `serializer_type` argument.
        If there is no group declared for the action, it will use the
        `serializer_class attribute which should be declared in the class.
        :param serializer_type: type of serializer to get from group, can be one of:
        request, input, output, response and default.
        :return: serializer class to be used.
        """
        if not (group := self.get_group()):
            return self.serializer_class
        return getattr(group, serializer_type, group.default)

    def get_serializer_class(self) -> Type[serializers.Serializer]:
        """
        Gets the default serializer class to be used based on the group for the
        action of the view.
        :return: serializer class to be used.
        """
        return self._get_serializer_class("default")

    def get_request_serializer_class(self) -> Type[serializers.Serializer]:
        """
        Gets the request serializer class to be used based on the group for the
        action of the view.
        :return: serializer class to be used.
        """
        return self._get_serializer_class("request")

    def get_input_serializer_class(self) -> Type[serializers.Serializer]:
        """
        Gets the input serializer class to be used based on the group for the
        action of the view.
        :return: serializer class to be used.
        """
        return self._get_serializer_class("input")

    def get_output_serializer_class(self) -> Type[serializers.Serializer]:
        """
        Gets the output serializer class to be used based on the group for the
        action of the view.
        :return: serializer class to be used.
        """
        return self._get_serializer_class("output")

    def get_response_serializer_class(self) -> Type[serializers.Serializer]:
        """
        Gets the response serializer class to be used based on the group for the
        action of the view.
        :return: serializer class to be used.
        """
        return self._get_serializer_class("response")

    def get_serializer(self, *args, **kwargs) -> serializers.Serializer:
        """
        Gets the default serializer to be used based on the group for the
        action of the view, adding the context.
        :return: serializer class to be used.
        """
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_request_serializer(self, *args, **kwargs) -> serializers.Serializer:
        """
        Gets the request serializer to be used based on the group for the
        action of the view, adding the context.
        :return: serializer class to be used.
        """
        serializer_class = self.get_request_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_input_serializer(self, *args, **kwargs) -> serializers.Serializer:
        """
        Gets the input serializer to be used based on the group for the
        action of the view, adding the context.
        :return: serializer class to be used.
        """
        serializer_class = self.get_input_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_output_serializer(self, *args, **kwargs) -> serializers.Serializer:
        """
        Gets the output serializer to be used based on the group for the
        action of the view, adding the context.
        :return: serializer class to be used.
        """
        serializer_class = self.get_output_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_response_serializer(self, *args, **kwargs) -> serializers.Serializer:
        """
        Gets the response serializer to be used based on the group for the
        action of the view, adding the context.
        :return: serializer class to be used.
        """
        serializer_class = self.get_response_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def _input_request_pre_processor(self, request: Request) -> Request:
        """
        Takes the initial `Request` object and turns it into one that can be
        processed by the input serializer.
        This method should be overriden.
        :param request: `Request` object.
        :return: `Request` object to be processed by the input serializer.
        """
        return request

    def _output_response_post_processor(
        self, request: Request, response: Response
    ) -> Response:
        """
        Takes the `Response` object after the output and turns it into one that
        complies with the response serializer.
        This method should be overriden to add functionality.
        :param request: `Request` object.
        :param response: `Response` object
        :return: `Response` after being processed by the response serializer.
        """
        return response

    def initialize_request(self, request, *args, **kwargs) -> Request:
        request = super().initialize_request(request, *args, **kwargs)
        return self._input_request_pre_processor(request)

    def finalize_response(self, request, response, *args, **kwargs) -> Response:
        response = super().finalize_response(request, response, *args, **kwargs)
        return self._output_response_post_processor(request, response)
