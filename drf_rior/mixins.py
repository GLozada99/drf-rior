from rest_framework import mixins, status
from rest_framework.response import Response


class UpdateModelMixin(mixins.UpdateModelMixin):
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        input_serializer = self.get_input_serializer(
            instance, data=request.data, partial=partial
        )
        input_serializer.is_valid(raise_exception=True)
        self.perform_update(input_serializer)

        if getattr(instance, "_prefetched_objects_cache", None) is not None:
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        # pylint: enable=protected-access
        output_serializer = self.get_output_serializer(instance)

        return Response(output_serializer.data)


class CreateModelMixin(mixins.CreateModelMixin):
    def create(self, request, *args, **kwargs):
        input_serializer = self.get_input_serializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        self.perform_create(input_serializer)

        output_serializer = self.get_output_serializer(input_serializer.instance)
        headers = self.get_success_headers(output_serializer.data)

        return Response(
            output_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class ListModelMixin(mixins.ListModelMixin):

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_output_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_output_serializer(queryset, many=True)
        return Response(serializer.data)


class RetrieveModelMixin(mixins.RetrieveModelMixin):
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data)
