from django.db import models

# Create your models here.
class Color(models.Model):
    name = models.CharField(max_length = 255, unique = True)

    def __str__(self) -> str:
        return self.name

class Condition(models.Model):
    name = models.CharField(max_length = 255, unique = True)

    def __str__(self) -> str:
        return self.name
    
class EngineType(models.Model):
    name = models.CharField(max_length = 255, unique = True)

    def __str__(self) -> str:
        return self.name

class CarMake(models.Model):
    name = models.CharField(max_length = 255, unique = True)

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
    engineType = models.ForeignKey(EngineType, on_delete = models.PROTECT)
    condition = models.ForeignKey(Condition,  on_delete=models.SET_NULL, null = True, blank = True)
    color = models.ForeignKey(Color, on_delete = models.SET_NULL, null = True, blank = True)
    featured = models.BooleanField(default = 0)

    class Meta:
        unique_together = ['carModel', 'year', 'milage', 'engineType', 'condition', 'color']