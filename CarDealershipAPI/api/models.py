from django.db import models

# Create your models here.
class Color(models.Model):
    name = models.CharField(max_length = 255)

    def __str__(self) -> str:
        return self.name

class Condition(models.Model):
    name = models.CharField(max_length = 255)

    def __str__(self) -> str:
        return self.name

class CarMake(models.Model):
    name = models.CharField(max_length = 255)

    def __str__(self) -> str:
        return self.name

class CarModel(models.Model):
    name = models.CharField(max_length = 255)
    carMake = models.ForeignKey(CarMake, on_delete = models.PROTECT)

    def __str__(self) -> str:
        return self.name

class Car(models.Model):
    carModel = models.ForeignKey(CarModel, on_delete = models.CASCADE)
    year = models.IntegerField()
    milage = models.DecimalField(max_digits = 7, decimal_places = 1)
    condition = models.ForeignKey(Condition,  on_delete=models.SET_NULL, null = True, blank = True)
    color = models.ForeignKey(Color, on_delete = models.SET_NULL, null = True, blank = True)