import requests
from .models import New, Show, Ask, Job
from django.core.exceptions import ObjectDoesNotExist


class Scraper(object):

    categories_available = {'askstories': Ask, 'showstories' : Show, 'newstories': New, 'jobstories': Job}

    def get_item(self, post_id, category):
        req_item = dict(requests.get(f"https://hacker-news.firebaseio.com/v0/item/{post_id}.json").json())
        return req_item

    def start(self, category_given):
        posts = []
        r = requests.get(f"https://hacker-news.firebaseio.com/v0/{category_given}.json")
        for item in r.json():
            try:
                item_category = self.categories_available[category_given]
                if item_category.objects.get(story_id=item):
                    print(f"Already in base: {item}")
                else:
                    scraped_item = self.get_item(item, category_given)
                    posts.append(scraped_item)
            except ObjectDoesNotExist:
                scraped_item = self.get_item(item, category_given)
                posts.append(scraped_item)
            except TypeError:
                continue
        return posts


if __name__ == '__main__':
    pass
