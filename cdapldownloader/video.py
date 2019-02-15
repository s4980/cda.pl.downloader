from os import path


class Video:
    def __init__(self, title: str, page_url: str):
        self.title = title
        self.page_url = path.join('https://www.cda.pl', remove_lead_and_trail_slash(page_url))
        self.download_url = None
        self.file_name = None

    def set_file_name(self, ext: str) -> str:
        self.file_name = f"{self.title}{ext}".replace(' ', '_').replace('/', '_').replace('\\', '_')

    def wget_command(self) -> str:
        return f"wget {self.download_url} --no-check-certificate -O {self.file_name}"

    @property
    def __str__(self) -> str:
        return f"Video details:\n\ttitle: {self.title}\n\tpage_link: {self.page_url}\n\tvideo_link: {self.download_url}"

    @property
    def __repr__(self) -> str:
        return self.__str__


def remove_lead_and_trail_slash(s: str) -> str:
    if s.startswith('/'):
        s = s[1:]
    if s.endswith('/'):
        s = s[:-1]
    return s
