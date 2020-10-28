import os
from users.models import (Author)
from django.contrib.auth.models import Group, Permission

from posts.models import Category


def run():
    rols()
    configuration()

def rols():
    """ metodo que crea los roles y le asigna los permisos """
    print("Creando roles....")

    # se verifica si el grupo existe
    if Group.objects.filter(name = 'Blogger').exists() != True: 
        # se crea el grupo
        group = Group.objects.create(name = "Blogger")
        # se filtran los permisos necesarios para el grupo
        permission = Permission.objects.filter(codename__in = [
            'view_post','add_post','change_post','delete_post',
            'add_like','change_like',
            'view_comment','add_comment','change_comment', 'delete_comment'
            ])

        # se asignan los permisos para el grupo
        for key in permission:
            group.permissions.add(key)

    if Group.objects.filter(name = 'Admin').exists() != True: 
        group = Group.objects.create(name = "Admin")
        permission = Permission.objects.all()

        for key in permission:
            group.permissions.add(key)

    print("Roles creados...ok")



def configuration():
    """ configuracion inicial 
        insercion de categorias de ejemplo
        insercion de usuario tipo admin de ejemplo
    """
    
    print("cargando configuraciones....")
    print("creando categorias...")
    # se verifica si el registro existe
    if Category.objects.filter(name = "Desarrollo").exists() != True:
        # se crea el registro
        Category.objects.create(name = "Desarrollo")

    if Category.objects.filter(name = "Python").exists() != True: 
        Category.objects.create(name = "Python")
   
    if Category.objects.filter(name = "Django").exists() != True: 
        Category.objects.create(name = "Django")
    
    if Category.objects.filter(name = "Programas").exists() != True: 
        Category.objects.create(name = "Programas")

    if Category.objects.filter(name = "Tecnologia").exists() != True: 
        Category.objects.create(name = "Tecnologia")
  
    if Category.objects.filter(name = "Ingenieria").exists() != True: 
        Category.objects.create(name = "Ingenieria")

    if Category.objects.filter(name = "Backend").exists() != True: 
        Category.objects.create(name = "Backend")

    if Category.objects.filter(name = "Frontend").exists() != True: 
        Category.objects.create(name = "Frontend")

    if Category.objects.filter(name = "Js").exists() != True: 
        Category.objects.create(name = "Js")

    print("categorias de ejemplo creadas...ok")
    
    print("creando usuario admin de ejemplo..")
    group = Group.objects.get(name='Admin')
    if Author.objects.filter(username="administrador").exists() !=True:
        # creacion de usuario
        author = Author(name="administrador", username = "administrador", surnames = "Ejemplo" ,\
            email = "administrador@developerblog.com",\
            type_user='Administrador')

        # set contraseña de usuario
        author.set_password("qwerty123")
        # guardado de informacion de usuario
        author.save()
        #asignar grupo a usuario
        group.user_set.add(author)

    print("usuario admin de ejemplo creado...")
 