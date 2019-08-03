from django.db import models


# Create your models here.
# Нужно переменовать в "Payment"
class Spend(models.Model):
    spend_owner = models.IntegerField(default=0)
    spend_text = models.CharField(max_length=200)
    spend_value = models.FloatField()
    spend_date = models.DateField()

    def __str__(self):
        return self.spend_text + ', ' + str(self.spend_value) + ', ' + str(self.spend_date)
