from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from django.views.generic.edit import (FormMixin)
from django.db.models import Prefetch
from datetime import date
from django.db.models import Count, Q
from django.contrib.postgres.search import SearchVector

# permisos
from users.permissions import (AuthorPermission, AdminPermission, DecoratorPermission)

from django.utils import timezone
import json
from django.http import (HttpResponse)
from django.urls import (reverse, reverse_lazy )
from django.shortcuts import get_object_or_404 

# import  de modelos
from .models import (Post, Comment, Like, Category)
from users.models import Author

#importacion de model de tag
from taggit.models import Tag

# importacion de formulario
from .forms import (CreatePostsForm, CreateCategoryForm, CommentPotsForm, postSearchForm)

# Create your views here.

# agregar o quitar like de un post
def PostLikeAction(request, id_post):
    """ vista para funcion agregar o quitar like  """
    if request.method == "POST":
        # si el usuario esta autenticado
        if request.user.is_authenticated:
            # se obtiene el objeto post
            post = get_object_or_404(Post, pk = id_post)
            # se obtiene el usuario
            user =  Author.objects.get(pk = request.user.id)
            if user in post.likes.all(): #si ya existe un like con este usuario
                # se remueve el like
                post.likes.remove(user)
                # like en falso para saber que el usuario no ha dado like a la publicacion 
                like=False
            else: #si no existe un like con este usuario
                # se agrega like con el usuario actual
                post.likes.add(user)
                # like en verdadero para mostrar que el usuario ya dio like 
                like=True
            # contexto o data a retornar
            context={"liked": like, "num_like_post": post.total_likes }
            #respuesta en formato json
        else:
            context={"liked": None, "num_like_post": None }
        return HttpResponse(json.dumps(context), content_type='application/json')


class SelfPostView(AuthorPermission, generic.ListView):
    """ vista para listar los post del usuario """

    permission_required = "posts.view_post"
    model = Post
    template_name = "posts/self_list_post.html"
    context_object_name = "post"
    form_class = postSearchForm

    def get_queryset(self):
        queryset = super(SelfPostView, self).get_queryset()
        form = self.form_class(self.request.GET)
        tags = self.request.GET.get('tags', None)
        categories = self.request.GET.get('categories', None)
        # search vector parametros
        search = SearchVector('title', 'tags__name', 'categories__name', 'author__name')
        author = Author.objects.get(pk=self.request.user.id)

        if author.type_user == 'Administrador':
            if form.is_valid() and form.cleaned_data['search']: # buscador general por:(titulo, tags, categrias, autor)
                query = queryset.annotate(
                            search = search).\
                    filter(
                            Q(search = form.cleaned_data['search']) | Q(search__icontains = form.cleaned_data['search']),

                    ).order_by('-id').distinct('id')
                    
            elif tags: # filtro por tags
                query = queryset.filter(
                    Q(tags__name = tags)
                )
                    
            elif categories: # filtro pos categorias
                query = queryset.filter(
                            Q(categories__name = categories)
                    )
                    
            else: #filtro solo por fecha y por estado
                query = queryset
        else:
            if form.is_valid() and form.cleaned_data['search']: # buscador general por:(titulo, tags, categrias, autor)
                query = queryset.annotate(
                            search = search
                            ).\
                    filter(
                            Q(search = form.cleaned_data['search']) | Q(search__icontains = form.cleaned_data['search']),
                            author = author.id
                    ).order_by('-id').distinct('id')
                    
            elif tags: # filtro por tags
                query = queryset.filter(
                            Q(tags__name = tags),
                            author = author.id
                    )
                    
            elif categories: # filtro pos categorias
                query = queryset.filter(
                            Q(categories__name = categories),
                            author = author.id
                    )
                    
            else: #filtro solo por fecha y por estado
                query = queryset.filter( 
                            author = author.id
                    ) 
        return query

    def get_context_data(self,**kwargs):
        context = super(SelfPostView, self).get_context_data(**kwargs)
        today = date.today()
        # contador para cantidad de me gusta
        context['cant_total_likes'] = Like.objects.filter(status = True).count()

        # cantidad total de comentarios
        context['cant_total_comments'] = Comment.objects.all().count()

        # cantidad total de posts
        context['cant_total_posts'] = Post.objects.filter(
            Q(status=True) | Q(post_start_date__lte = today, post_end_date__gte = today)
            ).count()

        # 5 categorias con mas post y la cantidad de cada una 
        context['categories'] = Category.objects.categories_more_post()

        # 8 tags mas usados en los post
        context['tags'] = Tag.objects.annotate(num_tags = Count('taggit_taggeditem_items')).\
                                            filter(num_tags__gte = 1).order_by('-num_tags')[:8]
        
        # post con mas me gusta
        context['post_more_likes'] = Post.objects.post_more_likes()

        return context


class DetailPost(FormMixin, generic.DetailView):
    """ vista para ver detalle de un post """

    model = Post
    context_object_name = "post"
    form_class = CommentPotsForm
    template_name = 'posts/detail_post.html'

    def get_success_url(self):
        return reverse('post:detail_post', kwargs = {'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #post con mas me gusta
        context['post_more_likes'] = Post.objects.post_more_likes()
        # comentarios del post
        context['comments'] = Comment.objects.filter(post_id = self.object)
        #tags del post
        context['tags'] = self.object.tags.all()
        # categorias del post
        context['categories'] = self.object.categories.all()
        # bool como bandera para saber si el usuario que accede a la vista ya ha dado like
        context['user_current_like'] = self.object.like_post.filter(user_id = self.request.user.id).exists()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form.errors)
            return self.form_invalid(form)

    def form_valid(self, form):
        form = form.save(commit = False)
        user = Author.objects.get(pk = self.request.user.id)
        form.post = self.object
        form.author = user
        form.save()
        return super(DetailPost, self).form_valid(form)


class PostNew(AuthorPermission, SuccessMessageMixin, generic.CreateView):
    """ vista para crear un nuevo post """

    permission_required = "posts.add_post"
    model = Post
    template_name = "posts/new_post.html"
    context_object_name = "post"
    form_class = CreatePostsForm
    success_url = reverse_lazy('post:self_list_post')
    success_message = "Post Creado Satisfactoriamente"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(status=True)
        return context

    def form_valid(self, form):
        form_pre_save = form.save(commit=False)
        user = Author.objects.get(pk = self.request.user.id)
        form_pre_save.author = user
        form_pre_save.save()
        form.save_m2m()
        return super().form_valid(form)


class PostEdit(AuthorPermission, generic.UpdateView):
    """ vista para editar un post """
    group_required = ['Blogger']
    permission_required = "posts.change_post"
    model = Post
    template_name = "posts/new_post.html"
    context_object_name = "post"
    form_class = CreatePostsForm
    success_url = reverse_lazy("post:self_list_post")
    success_message = "Post Actualizado Satisfactoriamente"

    @DecoratorPermission
    def get(self, request, *args, **kwargs):
       self.object = self.get_object()
       return super(PostEdit, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        form_pre_save = form.save(commit=False)
        form.updated_at = timezone.now()
        form_pre_save.save()
        form.save_m2m()
        return super().form_valid(form)


class PostDelete(SuccessMessageMixin, generic.DeleteView, AuthorPermission):
    """ vista para eliminar un post """

    permission_required="posts.delete_post"
    model = Post
    template_name='posts/delete_item.html'
    context_object_name = 'obj'
    success_url = reverse_lazy("post:self_list_post")
    success_message = "Post Eliminado Satisfactoriamente"

    @DecoratorPermission
    def get(self, request, *args, **kwargs):
       self.object = self.get_object()
       return super(PostDelete, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Nombre'] = "Post"
        return context


class CategoryView(AdminPermission, generic.ListView):
    """ vista para listar las categorias """

    permission_required = "posts.view_category"
    model = Category
    template_name = "posts/list_categories.html"
    context_object_name = "obj"


class CategoryNew(AdminPermission, SuccessMessageMixin, generic.CreateView):
    """ vista para crear una nueva categoria """

    permission_required = "posts.add_category"
    model = Category
    template_name = "posts/new_category.html"
    context_object_name = "obj"
    form_class = CreateCategoryForm
    success_url = reverse_lazy('post:list_category')
    success_message = "Categoria Creada Satisfactoriamente"


class CategoryEdit(SuccessMessageMixin, generic.UpdateView, AdminPermission):
    """ vista para editar una categoria """

    permission_required = "posts.change_category"
    model = Category
    template_name = "posts/new_category.html"
    context_object_name = "obj"
    form_class = CreateCategoryForm
    success_url = reverse_lazy('post:list_category')
    success_message = "Categoria Actualizada Satisfactoriamente"

    def form_valid(self, form):
        form_pre_save = form.save(commit=False)
        form_pre_save.updated_at = timezone.now()
        form_pre_save.save()
        form.save()
        return super().form_valid(form)


class CategoryDelete(SuccessMessageMixin, generic.DeleteView, AdminPermission):
    """ vista para eliminar una categoria """

    permission_required="posts.delete_category"
    model = Category
    template_name='posts/delete_item.html'
    context_object_name = 'obj'
    success_url = reverse_lazy('post:list_category')
    success_message = "Categoria Eliminada Satisfactoriamente"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Nombre'] = "Categoria"
        return context


class CommentDelete(SuccessMessageMixin, generic.DeleteView, AuthorPermission):
    """ vista para eliminar un post """

    permission_required="posts.delete_comment"
    model = Comment
    template_name='posts/delete_item.html'
    context_object_name = 'obj'
    success_message = "Post Eliminado Satisfactoriamente"

    @DecoratorPermission
    def get(self, request, *args, **kwargs):
       self.object = self.get_object()
       return super(CommentDelete, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('post:detail_post', kwargs = {'slug': self.object.post.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Nombre'] = "Comentario"
        return context