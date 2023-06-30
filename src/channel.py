import json
import os
from googleapiclient.discovery import build

# channel_id = 'UC-OVMPlMA3-YCIeg4z5z23A'  # MoscowPython
# channel_id = 'UCwHL6WHUarjGfUM_586me8w'  # HighLoad Channel


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала.
        Дальше все данные подтягиваются по API."""
        self.__channel_id = channel_id
        video_response = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title: str = video_response['items'][0]['snippet']['title']
        self.url: str = "https://www.youtube.com/channel/" + channel_id
        self.description: str = video_response['items'][0]['snippet']['description']
        self.view_count = int(video_response['items'][0]['statistics']['viewCount'])
        self.video_count = int(video_response['items'][0]['statistics']['videoCount'])
        self.subscriber_count = int(video_response['items'][0]['statistics']['subscriberCount'])

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        return self.subscriber_count - other.subscriber_count

    def __lt__(self, other):
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count

    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        return self.subscriber_count >= other.subscriber_count

    def __eq__(self, other):
        return self.subscriber_count == other.subscriber_count

    # def print_info(self) -> None:
    #   """Выводит в консоль информацию о канале."""
    #   channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
    #   print(json.dumps(channel, indent=2, ensure_ascii=False))

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API.
        """
        api_key: str = os.getenv('YOU_TUBE_API')
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, file_name):
        """
        Сохраняет в файл значения атрибутов экземпляра `Channel`.
        """
        data = {"channel_id": self.channel_id, "title": self.title,
                "url": self.url, "description": self.description,
                "view_count": self.view_count, "subscriber_count": self.subscriber_count,
                "video_count": self.video_count}

        with open(file_name, "w", encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False)
