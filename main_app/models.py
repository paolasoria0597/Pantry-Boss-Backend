from django.contrib.auth.models import User
from django.db import models

class Floor(models.Model):
    number = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Floor {self.number} (User: {self.user.username})"

class Pantry(models.Model):
    name = models.CharField(max_length=100)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)

    def __str__(self):
        return f"Pantry {self.name} on Floor {self.floor.number}"

class Dispenser(models.Model):
    DRINK = 'DR'
    SNACK = 'SN'
    COFFEE = 'CO'

    DISPENSER_TYPE_CHOICES = [
        (DRINK, 'Drink'),
        (SNACK, 'Snack'),
        (COFFEE, 'Coffee'),
    ]

    type = models.CharField(max_length=2, choices=DISPENSER_TYPE_CHOICES)
    max_capacity = models.PositiveIntegerField()
    current_level = models.PositiveIntegerField(help_text='Current level in units')
    threshold = models.PositiveIntegerField(default=10, help_text='Low level threshold percentage')
    pantry = models.ForeignKey('Pantry', on_delete=models.CASCADE)

    def is_running_low(self):
        """Check if the dispenser is below the threshold"""
        return (self.current_level / self.max_capacity) * 100 < self.threshold

    def __str__(self):
        return f"{self.get_type_display()} Dispenser in {self.pantry.name}"
