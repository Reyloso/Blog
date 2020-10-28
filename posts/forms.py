from django import forms
# import libreria summernote widgets para los textfield
from django_summernote.widgets import (SummernoteWidget)

#import de modelos
from .models import (Post, Category, Comment)


class postSearchForm(forms.Form):
    """ fomulario para el buscador  """

    search = forms.CharField(required=False)


class CreatePostsForm(forms.ModelForm):
    """ formulario para los post """

    post_start_date = forms.DateTimeField(required=False, input_formats = ['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs = {
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker'
        })
    )

    post_end_date = forms.DateTimeField(required=False, input_formats = ['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs = {
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker'
        })
    )

    class Meta:
        model = Post
        fields = ['cover','title','description','article','post_start_date','post_end_date','tags','status','categories','updated_at']
        widgets = {
            'article': SummernoteWidget(),
        }

    def __init__(self, *args, **kwargs):
        super(CreatePostsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CreateCategoryForm(forms.ModelForm):
    """ formulario para categorias """
    
    class Meta:
        model = Category
        fields = ['name','status','updated_at']

    def __init__(self, *args, **kwargs):
        super(CreateCategoryForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CommentPotsForm(forms.ModelForm):
    """ formulario para los comentarios en los post """

    class Meta:
        model = Comment
        fields = ['comment','post','author']
    
