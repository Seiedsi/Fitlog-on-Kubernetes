from django.db import models
from django.contrib.auth.models import User

class Food(models.Model):
    name = models.CharField(max_length=200)
    calories = models.FloatField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fats = models.FloatField()

    def __str__(self):
        return self.name

class Consumption(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    amount = models.FloatField()  # in grams
    date_consumed = models.DateField(auto_now_add=True)

    def calculated_calories(self):
        return round((self.food.calories / 100) * self.amount, 2)
    def calculated_protein(self):
        return round((self.food.protein / 100) * self.amount, 2)
    def calculated_carbs(self):
        return round((self.food.carbs / 100) * self.amount, 2)
    def calculated_fats(self):
        return round((self.food.fats / 100) * self.amount, 2)

    def __str__(self):
        return str(self.user.username) + '-' + str(self.food.name)