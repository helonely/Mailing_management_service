from django import forms
from .models import Blog


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'picture',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),

            'picture': forms.FileInput(attrs={'class': 'form-control'})

        }


class BlogUpdateForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'picture',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'picture': forms.FileInput(attrs={'class': 'form-control'})
        }
