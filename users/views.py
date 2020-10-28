from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views import generic

from django.urls import (reverse_lazy )

# import de modelos
from django.contrib.auth.models import Group
from .models import (Author)

# import formulario
from .forms import (AuthorCreationForm)


# Create your views here.
class SuccesRegisterView(TemplateView):
    """ vista al finalizar registro """
    
    template_name = 'users/success_user_register.html'

class NoPermissionsView(TemplateView):
    """ vista de informacion de no permisos """
    
    template_name = 'users/message_no_permissions.html'

class UserCreateView(generic.CreateView):
    """ vista para formulario de registro de usuarios """

    permission_required = "author.add_author"
    model = Author
    template_name = "users/register_user_form.html"
    context_object_name = "obj"
    form_class = AuthorCreationForm
    success_url = reverse_lazy('user:success_register_user')
    success_message = "Registro Completado Satisfactoriamente"

    def form_valid(self, form):
        user = form.save()
        group = Group.objects.get(name='Blogger')
        group.user_set.add(user)
        return super().form_valid(form)