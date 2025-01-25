from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class MyAdminUser(UserAdmin):
    list_display = ["username", "email", "first_name", "last_name", "isibo", "is_active"]
    list_filter = ["is_staff"]
    fieldsets = [
        (None, {"fields": ["password", "username", "email"]}),
        ("Personal info", {"fields": ["first_name", "last_name", "picture", "gender"]}),
        ("Address info", {"fields": ["province", "district", "sector", "cell", "village", "isibo"]}),
        ("Permissions", {"fields": ["is_active", "is_superuser", "is_staff"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["username", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(CustomUser, MyAdminUser)


