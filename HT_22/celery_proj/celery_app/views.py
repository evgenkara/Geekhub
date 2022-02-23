from django.shortcuts import render
from .forms import UserForm
from .tasks import scrap_start


def index(request):
    submit_button = request.POST.get("submit")
    story = ''

    form = UserForm(request.POST or None)
    if form.is_valid():
        story = form.cleaned_data.get("story")
        scrap_start.delay(story)

    context = {'form': form, 'story': story, 'submitbutton': submit_button}

    return render(request, 'celery_app/index.html', context)
