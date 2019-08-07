from django.db import models


# Create your models here.
# Нужно переменовать в "Payment"
class PaymentLabel(models.Model):
    payment_label_owner = models.IntegerField(default=0)
    payment_label_text = models.CharField(max_length=50)
    payment_label_color = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.payment_label_text


class Spend(models.Model):
    spend_owner = models.IntegerField(default=0)
    spend_text = models.CharField(max_length=200)
    spend_value = models.FloatField()
    spend_date = models.DateField()
    spend_label = models.ForeignKey(PaymentLabel, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.spend_text + ', ' + str(self.spend_value) + ', ' + str(self.spend_date)
