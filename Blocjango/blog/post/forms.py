from django import forms
from .models import Post,Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post  
        fields = ['title', 'content', 'category', 'published', 'pages', 'image']  
        labels = {
            'title': 'Título',
            'content': 'Contenido',
            'category': 'Categoría',
            'published': '¿Publicar ahora?',
            'pages':'Numero de paginas',
            'image': 'Imagen de portada'
        }
        widgets = {
            'title': forms.TextInput(attrs={'id': 'title', 'required': 'true'}),
            'content': forms.Textarea(attrs={'id': 'content', 'rows': 5}),
            'category': forms.CheckboxSelectMultiple(attrs={'id': 'category'}),
            'published': forms.CheckboxInput(attrs={'id': 'published'}),
            'pages':forms.NumberInput(attrs={'id': 'pages', 'required': 'true'}),
            'image': forms.FileInput(attrs={'class':'form-control', 'required':'true'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3,  'class':'form-control','placeholder': 'Escribe tu reseña o información del libro aquí...'})
        }

class Registro(UserCreationForm):
    email = forms.EmailField(required = 'true', label='Correo Electronico')
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)