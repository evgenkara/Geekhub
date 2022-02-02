import requests


class Scraper(object):

    categories_available = ['askstories', 'showstories', 'newstories', 'jobstories']

    @staticmethod
    def get_item(post_id):
        req_item = dict(requests.get(f"https://hacker-news.firebaseio.com/v0/item/{post_id}.json").json())
        return req_item

    def start(self, category_given):
        posts = []
        r = requests.get(f"https://hacker-news.firebaseio.com/v0/{category_given}.json")
        for item in r.json():
            try:
                posts.append(self.get_item(item))
            except TypeError:
                continue
        return posts


if __name__ == '__main__':
    pass
