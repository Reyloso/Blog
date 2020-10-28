from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import (User,Author)
from users.forms import (CustomUserCreationForm,CustomUserChangeForm)


# Register your models here.
class Usuarios(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    fieldsets = (
        (None, {'fields': ('type_user','email', 'username','password')}),
        ('Information', {'fields': ('date_joined','last_login',)}),
        ('Permissions', {'fields': ('is_active',)}),
        
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ( 'email','type_user', 'username', 'password1', 'password2', 'is_active')}
        ),
    )

    list_filter = ('is_active',)
    search_fields = ('id','email','username')
    list_display = ['id','type_user','username', 'email','is_active','date_joined','last_login']

    class Meta:
        model = User


class Authors(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    fieldsets = (
        ('Permisos', {'fields': ( 'groups', 'user_permissions', 'is_active')}),
        ('Datos del sesión', {'fields': ('date_joined', 'last_login','updated_at', 'deleted_at')}),
        ('Datos personales',
         {'fields': ('profile_photo', 'type_user','name', 'surnames')}),
        ('Datos de contacto', {'fields': ('username','email', 'password')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('profile_photo','type_user','name','surnames','email','username', 'password1',
                'password2', 'groups', 'is_active')}
         ),
    )
    search_fields = ('type_user','email','username', 'document', 'name', 'surnames')
    filter_horizontal = ()
    list_filter = ('type_user',)

    list_display = ['id','type_user','username', 'name','surnames','updated_at','deleted_at']

    class Meta:
        model = Author


admin.site.register(User, Usuarios)
admin.site.register(Author, Authors)