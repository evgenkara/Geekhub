from django import forms


STORY_CHOICES = (
    ('askstories', 'askstories'),
    ('showstories', 'showstories'),
    ('jobstories', 'jobstories'),
    ('newstories', 'newstories')
)


class UserForm(forms.Form):
    story = forms.CharField(label='Chose category: ',
                            widget=forms.Select(choices=STORY_CHOICES))
