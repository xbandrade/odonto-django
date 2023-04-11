from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.serializers import UserSerializer


class UserAPIViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]
    http_method_names = ['get', 'post', 'patch']

    def get_queryset(self):
        User = get_user_model()
        qs = User.objects.filter(username=self.request.user.username)
        return qs

    @action(
        methods=['get'],
        detail=False,
    )
    def me(self, request, *args, **kwargs):
        obj = self.get_queryset().first()
        serializer = self.get_serializer(
            instance=obj,
        )
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj != request.user:
            raise PermissionDenied(
                'You do not have permission to update this user.')
        serializer = UserSerializer(
            instance=obj,
            data=request.data,
            context={'request': request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
