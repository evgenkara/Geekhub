import requests
from .models import New, Show, Ask, Job
from django.core.exceptions import ObjectDoesNotExist


class Scraper(object):

    categories_available = {'askstories': Ask, 'showstories' : Show, 'newstories': New, 'jobstories': Job}

    def get_item(self, post_id, category):
        req_item = dict(requests.get(f"https://hacker-news.firebaseio.com/v0/item/{post_id}.json").json())
        item_category = self.categories_available[category]
        item_id = req_item['id']
        try:
            if item_category.objects.get(story_id=item_id):
                print(f"Already in base: {item_id}")
            else:
                return req_item
        except ObjectDoesNotExist:
            return req_item

    def start(self, category_given):
        posts = []
        r = requests.get(f"https://hacker-news.firebaseio.com/v0/{category_given}.json")
        for item in r.json():
            try:
                scraped_item = self.get_item(item, category_given)
                if scraped_item is not None:
                    posts.append(scraped_item)
            except TypeError:
                continue
        return posts


if __name__ == '__main__':
    pass
