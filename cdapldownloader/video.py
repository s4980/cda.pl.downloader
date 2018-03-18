import os


class Video:
    def __init__(self, title, page_url):
        self.title = title
        self.page_url = os.path.join('https://www.cda.pl', remove_lead_and_trail_slash(page_url))
        self.download_url = ''

    def __str__(self):
        return '{} link: {} download: {}'.format(self.title, self.page_url, self.download_url)

    def __repr__(self):
        return self.__str__()


def remove_lead_and_trail_slash(s):
    if s.startswith('/'):
        s = s[1:]
    if s.endswith('/'):
        s = s[:-1]
    return s