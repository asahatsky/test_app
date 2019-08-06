from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from test_app.models import Building, Item, Company, Patent
from test_app.api.serializers import BuildingSerializer, PatentSerializer, CompanySerializer, ItemSerializer


class BuildingViewSet(ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class PatentViewSet(ModelViewSet):
    queryset = Patent.objects.all()
    serializer_class = PatentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
