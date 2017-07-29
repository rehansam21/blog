from django import forms
from .models import Posts
from pagedown.widgets import PagedownWidget


class PostForms(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=False))
    publish = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Posts
        fields = [
            'title',
            'content',
            'image',
            'publish',
            'draft',
        ]
