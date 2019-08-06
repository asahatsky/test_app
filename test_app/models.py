from django.conf import settings
from django.core.validators import MaxValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Ownership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='ownerships',
                             on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    part = models.PositiveSmallIntegerField(null=False, validators=[MaxValueValidator(100), ])

    class Meta:
        unique_together = ('content_type', 'user')

    def __str__(self):
        return f'{self.user} owns {self.part}% of {str(self.content_type).lower()} {self.object_id}'


class Building(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='building_id')
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    ownerships = GenericRelation(Ownership)

    def __str__(self):
        return self.name


class Company(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='company_id')
    name = models.CharField(max_length=100)
    building = models.ForeignKey(Building,
                                 on_delete=models.DO_NOTHING,
                                 related_name='companies',
                                 related_query_name='company')
    ownerships = GenericRelation(Ownership)

    def __str__(self):
        return self.name


class Patent(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='item_id')
    name = models.CharField(max_length=100)
    ownerships = GenericRelation(Ownership)
    identification_number = models.CharField(unique=True, max_length=15)


class Item(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='item_id')
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company,
                                on_delete=models.DO_NOTHING,
                                related_name='items',
                                related_query_name='item')
    ownerships = GenericRelation(Ownership)
    identification_number = models.CharField(unique=True, max_length=15)
    patent = models.ManyToManyField(Patent,
                                    related_name='items',
                                    related_query_name='item',
                                    db_table='item_patents')

    def __str__(self):
        return self.name


