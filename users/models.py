# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import (BaseUserManager, Group, AbstractBaseUser, AbstractUser, Permission)

# import helpers 
from posts.helpers import (valid_extension, photo_profile_name)

#control de historico de tablas
from simple_history import register

#model user
class User(AbstractUser):
    """ clase abstracta del modelo usuario usada para extender el modelo usuario """ 
    #choicefield para los tipos de usuario
    type_users = (
        ('Administrador', 'Administrador'),
        ('Blogger', 'Blogger'),
    )

    type_user = models.CharField(max_length = 20, choices = type_users, default='Blogger', null = False, blank = False)

    name = models.CharField(max_length = 100, null = False)
    surnames = models.CharField(max_length = 100, null = False)
    updated_at = models.DateTimeField(null = True, blank = True)
    deleted_at = models.DateTimeField(null = True, blank = True)

    USERNAME_FIELD = 'username'
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

#model author
class Author(User):
    """ clase de autores que hereda de usuario """


    #foto de perfil
    profile_photo = models.ImageField(upload_to = photo_profile_name, verbose_name = 'Profile', default = 'default_image/user.png', null = False, blank = False, validators = [valid_extension,])
    
    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"


    def full_name(self):
        return str('{} {}'.format(self.name, self.surnames))


    def __str__(self):
        return str('ID: {} | Username: {}'.format(self.id, self.username))



# regitro de tablas para guardar historico
register(User)
register(Author)