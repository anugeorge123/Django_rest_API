from django.contrib import admin
from accounts.models import Country, State, City, User

admin.site.register(Country, admin.ModelAdmin)
admin.site.register(State, admin.ModelAdmin)
admin.site.register(City, admin.ModelAdmin)
admin.site.register(User, admin.ModelAdmin)