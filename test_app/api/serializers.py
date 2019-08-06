from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from rest_framework import serializers
from test_app.models import Building, Patent, Item, Company, Ownership

User = get_user_model()


def is_owned(obj, user) -> bool:
    if not user.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    ownerships = Ownership.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user)
    return ownerships.exists()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')


class OwnerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Ownership
        fields = ('user', 'part')


class BuildingSerializer(serializers.ModelSerializer):
    is_owned = serializers.SerializerMethodField(read_only=True, required=False)
    owners = serializers.SerializerMethodField(read_only=True, required=False)

    class Meta:
        model = Building
        fields = ('id',
                  'name',
                  'address',
                  'is_owned',
                  'owners')

    def get_is_owned(self, obj):
        request = self.context['request']
        return is_owned(obj, request.user)

    def get_owners(self, obj):
        serializer = OwnerSerializer(instance=obj.ownerships.all(), many=True)
        return serializer.data


class CompanySerializer(serializers.ModelSerializer):
    is_owned = serializers.SerializerMethodField(read_only=True, required=False)
    owners = serializers.SerializerMethodField(read_only=True, required=False)

    class Meta:
        model = Company
        fields = ('id',
                  'name',
                  'building',
                  'is_owned',
                  'owners')

    def get_is_owned(self, obj):
        request = self.context['request']
        return is_owned(obj, request.user)

    def get_owners(self, obj):
        serializer = OwnerSerializer(instance=obj.ownerships.all(), many=True)
        return serializer.data


class PatentSerializer(serializers.ModelSerializer):
    is_owned = serializers.SerializerMethodField(read_only=True, required=False)
    owners = serializers.SerializerMethodField(read_only=True, required=False)

    class Meta:
        model = Patent
        fields = ('id',
                  'name',
                  'identification_number',
                  'is_owned',
                  'owners')

    def get_is_owned(self, obj):
        request = self.context['request']
        return is_owned(obj, request.user)

    def get_owners(self, obj):
        serializer = OwnerSerializer(instance=obj.ownerships.all(), many=True)
        return serializer.data


class ItemSerializer(serializers.ModelSerializer):
    patents = PatentSerializer(many=True)
    is_owned = serializers.SerializerMethodField(read_only=True, required=False)
    owners = serializers.SerializerMethodField(read_only=True, required=False)

    class Meta:
        model = Item
        fields = ('id',
                  'name',
                  'company',
                  'patents',
                  'identification_number',
                  'is_owned',
                  'owners')

    def get_is_owned(self, obj):
        request = self.context['request']
        return is_owned(obj, request.user)

    def get_owners(self, obj):
        serializer = OwnerSerializer(instance=obj.ownerships.all(), many=True)
        return serializer.data





