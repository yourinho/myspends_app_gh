from django.contrib import admin

# Register your models here.

from .models import Spend
from .models import PaymentLabel

admin.site.register(Spend)
admin.site.register(PaymentLabel)
