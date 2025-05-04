from django.db import models
from django.contrib.auth.models import User

class Workout(models.Model):
    name = models.CharField(max_length=200)
    calories = models.FloatField()

    def __str__(self):
        return self.name

class Exercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    time = models.FloatField()  # in minutes
    date_exercised = models.DateField(auto_now_add=True)

    def calculated_calories(self):
        return round((self.workout.calories / 60) * self.time, 2)