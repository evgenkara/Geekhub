from django import forms
from .models import Comment


class ContactForm(forms.Form):
    user_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Ваше ім'я")
    user_email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Eлектронна пошта')
    question = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Питання')


class CommentForm(forms.ModelForm):

    body = forms.CharField(max_length=300, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 7}))

    class Meta:
        model = Comment
        fields = ('body',)
