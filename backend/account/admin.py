from django.contrib import admin

from .models import User,Restaurant,DeliveryPartner


admin.site.register(User)
admin.site.register(Restaurant)
admin.site.register(DeliveryPartner)
