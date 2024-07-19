from django.db import models

# Create your models here.

class LegoItems(models.Model):
    item_number = models.AutoField(primary_key=True)
    set_number = models.PositiveIntegerField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    price = models.PositiveIntegerField(blank=True, null=True)
    site = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=2047, blank=True, null=True)
    date_modified = models.DateTimeField(blank=True, null=True)

    #class Meta:
        #db_table = 'lego_items'