from django.db import models


class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=75, null=False)
    brand = models.CharField(max_length=30, null=False)
    weight_value = models.FloatField(null=False)
    weight_unit = models.CharField(max_length=10, null=False)
    price = models.FloatField(null=False)
    max_qty = models.IntegerField(null=False)
    seller_id = models.IntegerField(null=False)
    generic_name = models.CharField(max_length=255, null=False)
    cart_category = models.CharField(max_length=255, null=False)
    available = models.BooleanField(null=False)

    def __str__(self):
        return self.name
