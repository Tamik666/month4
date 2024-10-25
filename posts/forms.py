from django import forms
from .models import Post, Tag

class PostForm(forms.Form):
    image = forms.ImageField()
    title = forms.CharField()
    content = forms.CharField()
    rate = forms.IntegerField(max_value=5, min_value=0)

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if (title and content) and (title.lower() == content.lower()):
            raise forms.ValidationError('Title and content must be different')
        else:
            return cleaned_data

    def clean_title(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        if title and title.lower() == 'python':
            raise forms.ValidationError('Title cannot be python')
        return title
    
class PostForm2(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["image", "title", "content", "rate", "tags"]
    widgets = {
        "content": forms.Textarea(
            attrs={
                "placegolder": "Write your text here",
                "class": "form-control"
                }
            ),
    }
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if (title and content) and (title.lower() == content.lower()):
            raise forms.ValidationError('Title and content must be different')
        else:
            return cleaned_data

    def clean_title(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        if title and title.lower() == 'python':
            raise forms.ValidationError('Title cannot be python')
        return title
    
class SearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search',
                'class': 'form-control'
                
            }
        ),
    )
    tag = forms.ModelChoiceField(
        required=False,
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    orderings = (
        ('title', 'By title'),
        ("-title", "By title descending"),
        ("rate", "By rate"),
        ("-rate", "By rate descending"),
        ("created_at", "By date"),
        ("-created_at", "By date descending"),
    )
    ordering = forms.ChoiceField(
        required=False,
        choices=orderings,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )