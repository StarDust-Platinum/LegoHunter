# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class LegoItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    set = models.ForeignKey('LegoSet', models.DO_NOTHING, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    price = models.PositiveIntegerField(blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lego_item'


class LegoSet(models.Model):
    set_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    theme = models.CharField(max_length=255, blank=True, null=True)
    year = models.TextField(blank=True, null=True)  # This field type is a guess.
    pieces = models.PositiveIntegerField(blank=True, null=True)
    availability = models.CharField(db_column='Availability', max_length=255, blank=True, null=True)  # Field name made lowercase.
    retail = models.PositiveIntegerField(blank=True, null=True)
    value = models.PositiveIntegerField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lego_set'
