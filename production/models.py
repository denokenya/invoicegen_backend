from django.db import models
from api.models import *
from stock.models import RawMaterial
from account.models import Company


class Product(models.Model):
    code = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, blank=True)
    hsnCode = models.CharField(max_length=20, blank=True)
    uom = models.CharField(max_length=5)
    rate = models.CharField(max_length=20)
    createdOn = models.DateTimeField(default=today, blank=True)


class RecipeIngredient(models.Model):
    material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    qty = models.IntegerField()


class Recipe(models.Model):
    code = models.CharField(max_length=50, null=False, blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(RecipeIngredient, on_delete=models.CASCADE)


class CompanyProduct(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)