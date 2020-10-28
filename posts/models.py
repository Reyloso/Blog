# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from users.models import Author
from django.utils import timezone
from django.db.models import Count

# importacion de funciones de ayuda para validar la extension y el nombre de la imagen
from .helpers import (valid_extension, cover_name)

from django.template.defaultfilters import slugify

#control de historico de tablas
from simple_history import register

#tag libreria
from taggit.managers import TaggableManager

from .managers import (PostManager, CategoryManager)


class Category(models.Model):
    """ modelo donde se guardan las categorias """

    name = models.CharField(unique = True, max_length = 140, null = False, blank = False)
    status = models.BooleanField(default = True)

    created_at = models.DateTimeField(default = timezone.now)
    updated_at = models.DateTimeField(null = True, blank = True)

    def __str__(self):
        return str('ID: {} : Name: {}'.format(self.id ,self.name))

    # instancia de la clase categoryManager
    objects = CategoryManager()

    class Meta:
        verbose_name_plural = "Categorias"
        verbose_name="Categoria"


#model post
class Post(models.Model):
    """ modelo donde se guardan los post creados por los usuarios  """

    cover = models.ImageField(upload_to = cover_name, verbose_name ='Cover', null = False, 
        blank = False, validators = [valid_extension,])

    title = models.CharField(max_length = 140)
    slug = models.SlugField(unique=True, max_length = 280, editable = False)
    description = models.CharField(max_length = 150)
    article = models.TextField()

    post_start_date = models.DateTimeField(null = True, blank = True)
    post_end_date = models.DateTimeField(null = True, blank = True)
    
    tags = TaggableManager()

    status = models.BooleanField(default = True)

    created_at = models.DateTimeField(default = timezone.now)
    updated_at = models.DateTimeField(null=True, blank = True)

    # foreigns keys 
    author = models.ForeignKey(Author, related_name = 'posts_author',
            on_delete=models.CASCADE, null=False, blank = False)

    # many to many
    categories = models.ManyToManyField(Category, related_name = 'posts_categories')

    likes = models.ManyToManyField(Author, through = 'Like', related_name = 'like_post_author', through_fields = ('post', 'user'))

    def __str__(self):
        return str('ID: {} : Title: {}'.format(self.id, self.title))

    #guardado de el slug desde el titulo
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    # instancia de la clase postmanager
    objects = PostManager()

    @property
    def total_likes(self):
        """
        Cantidad de Me gusta por post

        """
        return self.like_post.count()

    @property
    def total_comments(self):
        """
        Cantidad de comentarios por post

        """
        return self.comment_post.count()

    class Meta:
        verbose_name_plural = "Publicaciones"
        verbose_name = "Publicacion"


class Comment(models.Model):
    """ modelo donde se guardan los comentarios creados por los usuarios """

    comment = models.TextField()

    created_at = models.DateTimeField(default = timezone.now)
    updated_at = models.DateTimeField(null = True, blank = True)

    # foreigns keys 
    author = models.ForeignKey(Author, related_name = 'comment_user',
            on_delete=models.CASCADE, null = True, blank = True)

    post = models.ForeignKey(Post, related_name = 'comment_post',
            on_delete=models.CASCADE, null = True, blank = True)


    def __str__(self):
        return str('ID: {} | post ID: {} | Name: {}'.format(self.id, self.post.id,self.user.name))

    class Meta:
        verbose_name_plural = "Comentarios"
        verbose_name = "Comentario"


class Like(models.Model):
    """ modelo donde se guardan los likes creados por los usuarios """
    status = models.BooleanField(default = True)
    
    created_at = models.DateTimeField(default = timezone.now)
    updated_at = models.DateTimeField(null = True, blank = True)

    # foreigns keys 
    user = models.ForeignKey(Author, related_name = 'like_user',
            on_delete = models.CASCADE, null = False, blank = False)
    post = models.ForeignKey(Post, related_name = 'like_post',
            on_delete = models.CASCADE, null=False, blank = False)

    def __str__(self):
        return str('ID: {} | post ID: {} | Name: {}'.format(self.id, self.post.id, self.user.name))

    class Meta:
        verbose_name_plural = "Me gusta"
        verbose_name = "Me gustas"


# regitro de tablas para guardar historico
register(Category)
register(Post)
register(Comment)
register(Like)
