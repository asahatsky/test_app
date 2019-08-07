from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from test_app.models import Building, Item, Company, Patent, Ownership
from test_app.api.serializers import BuildingSerializer, PatentSerializer, CompanySerializer, ItemSerializer


def set_owner(viewset, request):
    data = request.data
    user_id = data.get('user_id')
    part = data.get('part')
    obj = viewset.get_object()
    obj_type = ContentType.objects.get_for_model(obj)
    try:
        ownership, is_created = Ownership.objects.get_or_create(
            content_type=obj_type, object_id=obj.id, user_id=user_id, defaults={'part': part})
    except IntegrityError:
        raise ValidationError('Owner already exists')
    ownership.save()
    serializer = viewset.get_serializer(instance=obj)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def delete_owner(viewset, request):
    data = request.data
    user_id = data.get('user_id')
    obj = viewset.get_object()
    obj_type = ContentType.objects.get_for_model(obj)
    try:
        ownership = Ownership.objects.get(
            content_type=obj_type, object_id=obj.id, user_id=user_id)
    except Ownership.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    ownership.delete()
    serializer = viewset.get_serializer(instance=obj)
    return Response(serializer.data, status=status.HTTP_200_OK)


class BuildingViewSet(ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    @action(methods=['POST', 'DELETE'], detail=True, url_path='owners', url_name='building-owners')
    def owner(self, request, pk=None):
        if request.method == 'POST':
            return set_owner(self, request)
        elif request.method == 'DELETE':
            return delete_owner(self, request)


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    @action(methods=['POST', 'DELETE'], detail=True, url_path='owners', url_name='company-owners')
    def set_owner(self, request, pk=None):
        if request.method == 'POST':
            return set_owner(self, request)
        elif request.method == 'DELETE':
            return delete_owner(self, request)


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    @action(methods=['POST', 'DELETE'], detail=True, url_path='owners', url_name='item-owners')
    def set_owner(self, request, pk=None):
        if request.method == 'POST':
            return set_owner(self, request)
        elif request.method == 'DELETE':
            return delete_owner(self, request)


class PatentViewSet(ModelViewSet):
    queryset = Patent.objects.all()
    serializer_class = PatentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    @action(methods=['POST', 'DELETE'], detail=True, url_path='owners', url_name='patent-owners')
    def set_owner(self, request, pk=None):
        if request.method == 'POST':
            return set_owner(self, request)
        elif request.method == 'DELETE':
            return delete_owner(self, request)
