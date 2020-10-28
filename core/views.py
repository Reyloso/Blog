# -*- coding: utf-8 -*
from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin,\
     PermissionRequiredMixin
from django.views import generic
from django.db.models import Count, Q

from django.contrib.postgres.search import SearchVector

#importacion de modelos
from posts.models import (Post, Like, Comment, Category)

#importacion de model de tag
from taggit.models import Tag

# fomulario de buscador
from posts.forms import postSearchForm


class Home(generic.ListView):
     model = Post
     form_class = postSearchForm
     context_object_name = "post"
     template_name = 'core/home.html'
     paginate_by = 6
     ordering = ['-created_at']

     def get_queryset(self):
          queryset = super(Home, self).get_queryset()
          today = date.today()
          form = self.form_class(self.request.GET)
          tags = self.request.GET.get('tags', None)
          categories = self.request.GET.get('categories', None)
          # search vector parametros
          search = SearchVector('title', 'tags__name', 'categories__name', 'author__name')

          if form.is_valid() and form.cleaned_data['search']: # buscador general por:(titulo, tags, categrias, autor)
               query = queryset.annotate(
                         search = search).\
                    filter(
                         Q(status = True) | Q(post_start_date__lte = today, post_end_date__gte = today),
                         Q(search = form.cleaned_data['search']) | Q(search__icontains = form.cleaned_data['search'])
                    ).order_by('-id').distinct('id')
                    
          elif tags: # filtro por tags
               query = queryset.filter(
                         Q(status = True) | Q(post_start_date__lte = today, post_end_date__gte = today),
                         Q(tags__name = tags)
                    )
                    
          elif categories: # filtro pos categorias
               query = queryset.filter(
                         Q(status = True) | Q(post_start_date__lte = today, post_end_date__gte = today),
                         Q(categories__name = categories)
                    )
                    
          else: #filtro solo por fecha y por estado
               query = queryset.filter( 
                         Q(status=True) | Q(post_start_date__lte = today, post_end_date__gte = today)
                    ) 
          
          return query

     def get_context_data(self,**kwargs):
          context = super(Home, self).get_context_data(**kwargs)
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