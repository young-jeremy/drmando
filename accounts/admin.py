from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_phone_number')

    def get_phone_number(self, obj):
        return obj.profile.phone_number if hasattr(obj, 'profile') else ''

    get_phone_number.short_description = 'Phone Number'


admin.site.register(User, CustomUserAdmin)


# If you want to also have a separate Profile admin
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'phone_number')
    list_filter = ('created_at', 'updated_at')



@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('phone_number', 'email', 'admission_number', 'first_name', 'last_name', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('phone_number', 'email', 'admission_number', 'first_name', 'last_name')
    ordering = ('phone_number',)

    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'admission_number')}),
        (_('User type'), {'fields': ('user_type',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'email', 'admission_number', 'password1', 'password2', 'user_type'),
        }),
    )