from django.contrib import admin
from accounts.models import Country, State, City, User, UserRole,Message
# from django.contrib.auth.admin import UserAdmin

# class UserAdmin(UserAdmin):
#     admin.site.register(User, UserAdmin)


admin.site.register(Country, admin.ModelAdmin)
admin.site.register(State, admin.ModelAdmin)
admin.site.register(City, admin.ModelAdmin)
admin.site.register(User, admin.ModelAdmin)
admin.site.register(UserRole, admin.ModelAdmin)
admin.site.register(Message, admin.ModelAdmin)