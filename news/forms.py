from django import forms
from django.core.exceptions import ValidationError
from .models import Post
class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'positions',
            'author',
            'category',
            'title',
            'content',
            'rating'
        ]
        widgets = {'positions': forms.HiddenInput()}
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if title == content:
            raise ValidationError('Заголовок не может быть идентичен названию!')
        return cleaned_data

