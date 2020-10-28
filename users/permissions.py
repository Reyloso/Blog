from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin,\
    PermissionRequiredMixin

from django.shortcuts import get_object_or_404 
from .models import Author


def DecoratorPermission(funct): 
    """ decorador que verifica que el post solo pueda ser modificado o eliminado 
        por el mismo usuario que lo creó o por un usuario con type_user 'administrador'
    """
    def get_obj(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user.is_authenticated:
            author =  get_object_or_404(Author, pk = self.request.user.id)
            if self.object.author.id == author.id or author.type_user == 'Administrador':
                pass
            else:
               return HttpResponseRedirect(reverse_lazy('user:user_no_permissions'))
        else:
            return HttpResponseRedirect(reverse_lazy('login'))
        return funct(self, request, *args, **kwargs)
    return get_obj


class AuthorPermission(LoginRequiredMixin, PermissionRequiredMixin):
    """ clase AuthorPermission para validar que minimo debe estar logueado como usuario author
        para poder acceder a las vistas 
    
    """

    login_url = 'login'
    raise_exception=False
    redirect_field_name="redirecto_to"

    def handle_no_permission(self):
        """ funcion para validar que el usuario no sea diferente a un administrador """
        from django.contrib.auth.models import AnonymousUser
        if not self.request.user == AnonymousUser():
            self.login_url='user:user_no_permissions'
            
        return HttpResponseRedirect(reverse_lazy(self.login_url))


class AdminPermission(LoginRequiredMixin, PermissionRequiredMixin):
    """ clase AuthorAdminPermissionPermission para validar que minimo debe estar logueado como usuario author
        y ademas su type_user debe ser administrador para poder acceder a las vistas 
    """

    login_url = 'login'
    raise_exception=False
    redirect_field_name="redirecto_to"

    def handle_no_permission(self):
        """ funcion para retornar mensaje al usuario al login en caso de que no este logueado 
            o mostrar mensaje de permisos en caso no ser usuario administrador
        
         """

        from django.contrib.auth.models import AnonymousUser
        if not self.request.user == AnonymousUser():
            self.login_url='user:user_no_permissions'
            return HttpResponseRedirect(reverse_lazy(self.login_url))
        
        if self.request.user.is_authenticated:
            author =  get_object_or_404(Author, pk = self.request.user.id)
            if not author.type_user == 'Administrador':
                self.login_url='user:user_no_permissions'
                return HttpResponseRedirect(reverse_lazy(self.login_url))
        return HttpResponseRedirect(reverse_lazy(self.login_url))
        
        

            
        
        
        