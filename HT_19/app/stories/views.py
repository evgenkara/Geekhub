from django.shortcuts import render
from .forms import UserForm
from .scraper import Scraper
from .models import Story, Ask, Job
from django.db import IntegrityError


def set_fields(model_fields, item):
    item = {'story_id' if k == 'id' else k: v for k, v in item.items()}
    fields = [f"{f.name}_id" if f.is_relation else f.name for f in model_fields]
    for field in fields:
        if field not in item.keys() and field != 'id':
            new_value = ''
            if field in ['descendants', 'score', 'time']:
                new_value = 0
            item.update({field: new_value})
    return item


def index(request):
    submitbutton = request.POST.get("submit")
    story = ''

    form = UserForm(request.POST or None)
    if form.is_valid():
        story = form.cleaned_data.get("story")
        scraper = Scraper()
        scraped_stories = scraper.start(story)
        for scraped_story in scraped_stories:
            if 'kids' in scraped_story.keys():
                scraped_story.pop('kids')
            try:
                if story == 'jobstories':
                    model_fields = set_fields(Job._meta.fields, scraped_story)
                    Job.objects.create(**model_fields)
                elif story == 'showstories' or story == 'newstories':
                    model_fields = set_fields(Story._meta.fields, scraped_story)
                    Story.objects.create(**model_fields)
                elif story == 'askstories':
                    model_fields = set_fields(Ask._meta.fields, scraped_story)
                    Ask.objects.create(**model_fields)
            except IntegrityError:
                continue

    context = {'form': form, 'story': story, 'submitbutton': submitbutton}

    return render(request, 'stories/index.html', context)
