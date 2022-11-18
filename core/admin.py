from django.contrib import admin
from .models import Carrier, Tag, Filter, Campaign, Customer, Email

admin.site.register(Carrier)
admin.site.register(Tag)
admin.site.register(Filter)
admin.site.register(Customer)
admin.site.register(Campaign)
admin.site.register(Email)