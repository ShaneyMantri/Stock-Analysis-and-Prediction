from django.db import models
from django.utils  import timezone
from django.contrib.auth.models import User

class Company(models.Model):
    Name = models.CharField(max_length = 100)
    Symbols = models.CharField(max_length = 25)
    # date = models.DateTimeField(default = timezone.now)
    # Current_Price = models.CharField(max_length = 10)
    # Percentage_Change = models.CharField(max_length = 10)

    def __str__(self):
        return self.Name
