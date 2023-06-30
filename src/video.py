import os
from googleapiclient.discovery import build


class Video:
    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id канала.
        Дальше все данные подтягиваются по API."""
        self.__video_id = video_id
        try:
            video_response = self.get_video().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                            id=self.video_id).execute()
            self.url: str = "https://www.youtube.com/watch?v=" + video_id
            self.title: str = video_response['items'][0]['snippet']['title']
            self.view_count: int = video_response['items'][0]['statistics']['viewCount']
            self.like_count: int = video_response['items'][0]['statistics']['likeCount']
        except (KeyError, IndexError):
            self.url = None
            self.title = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        return f"{self.title}"

    @property
    def video_id(self):
        return self.__video_id

    @classmethod
    def get_video(cls):
        """
        Возвращает объект для работы с YouTube API.
        """
        api_key: str = os.getenv('YOU_TUBE_API')
        return build('youtube', 'v3', developerKey=api_key)


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.playlist_id = playlist_id
