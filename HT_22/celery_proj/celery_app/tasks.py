import requests
import time
from celery import shared_task
from .models import New, Show, Ask, Job
from django.core.exceptions import ObjectDoesNotExist


categories_available = {'askstories': Ask, 'showstories': Show, 'newstories': New, 'jobstories': Job}


@shared_task
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


@shared_task
def save_items(scraped_stories, story):
    for scraped_story in scraped_stories:
        dict_fields = ['kids', 'parts', 'parents', 'comments']
        for field in dict_fields:
            if field in scraped_story.keys():
                scraped_story.pop(field)

        model_category = categories_available[story]
        model_fields = set_fields(model_category._meta.fields, scraped_story)
        model_category.objects.create(**model_fields)


@shared_task
def get_item(post_id):
    req_item = dict(requests.get(f"https://hacker-news.firebaseio.com/v0/item/{post_id}.json").json())
    return req_item


@shared_task
def scrap_start(category_given):
    posts = []
    r = requests.get(f"https://hacker-news.firebaseio.com/v0/{category_given}.json")
    for item in r.json():
        try:
            item_category = categories_available[category_given]
            if item_category.objects.get(story_id=item):
                print(f"Already in base: {item}")
            else:
                scraped_item = get_item(item, category_given)
                posts.append(scraped_item)
        except ObjectDoesNotExist:
            scraped_item = get_item(item)
            posts.append(scraped_item)
        except TypeError:
            continue
    save_items(posts, category_given)
    time.sleep(0.5)


if __name__ == '__main__':
    pass
