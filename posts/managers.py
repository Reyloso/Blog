from django.db import models
from datetime import date
from django.db.models import Count, Q



class CategoryManager(models.Manager):
    """ Clase que agrega metodos personalizados al modelo category """

    # metodo que retorna las categorias con mas post ordenados de forma descendente
    def categories_more_post(self):
        return self.annotate(num_post=Count('posts_categories')).\
                                                  filter(num_post__gte=1).order_by('-num_post')[:5]


class PostManager(models.Manager):
    """ Clase que agrega metodos personalizados al modelo post """

    # metodo que retorna los post con mas likes ordenados de forma descendente
    def post_more_likes(self):
        today = date.today()
        query = self.annotate(num_likes=Count('like_post')).\
            filter(Q(status=True) | Q(post_start_date__lte = today,
                post_end_date__gte = today),
                num_likes__gte=1
            ).\
            order_by('-num_likes')[:5]
        return query

    

