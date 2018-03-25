from os import path


class Video:
    def __init__(self, title, page_url):
        self.title = title
        self.page_url = path.join('https://www.cda.pl', remove_lead_and_trail_slash(page_url))
        self.download_url = None
        self.file_name = None

    def set_file_name(self, ext):
        self.file_name = f'{self.title}{ext}'.replace(' ', '_')

    def wget_command(self):
        return 'wget {} --no-check-certificate -O {}'.format(self.download_url, self.file_name)

    def __str__(self):
        return '{} \n\tpage_link: {} \n\tvideo_link: {}'.format(self.title, self.page_url, self.download_url)

    def __repr__(self):
        return self.__str__()


def remove_lead_and_trail_slash(s):
    if s.startswith('/'):
        s = s[1:]
    if s.endswith('/'):
        s = s[:-1]
    return s
