import os
import isodate
import datetime
from googleapiclient.discovery import build


class PlayList:

    def __init__(self, playlist_id: str) -> None:
        """Экземпляр инициализируется id плей-листа.
           Дальше все данные подтягиваются по API."""
        self.playlist_id = playlist_id

        response = self.get_playlist().playlists().list(id=playlist_id, part='contentDetails,snippet',
                                                        maxResults=50,).execute()
        self.title: str = response['items'][0]['snippet']['title']
        self.url: str = f"https://www.youtube.com/playlist?list={playlist_id}"

    @classmethod
    def get_playlist(cls):
        """
        Возвращает объект для работы с YouTube API.
        """
        api_key: str = os.getenv('YOU_TUBE_API')
        return build('youtube', 'v3', developerKey=api_key)

    def videos_data_list(self):
        """
        Возвращает данные по каждому видео из плей-листа
        ('contentDetails,statistics')
        """
        playlist_videos = self.get_playlist().playlistItems().list(playlistId=self.playlist_id, part='contentDetails',
                                                                   maxResults=50, ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        playlist_response = self.get_playlist().videos().list(part='contentDetails,statistics',
                                                              id=','.join(video_ids)).execute()
        return playlist_response

    @property
    def total_duration(self):
        """
        Вывод суммарной длительности видеороликов из плейлиста.
        Return: duration - объект класса `datetime.timedelta`
        """
        duration = datetime.timedelta(seconds=0)

        videos_data = self.videos_data_list()
        for video in videos_data['items']:
            iso_8601_duration = video['contentDetails']['duration']  # YouTube video duration is in ISO 8601 format
            duration += isodate.parse_duration(iso_8601_duration)
        return duration

    def show_best_video(self):
        """
        Сортировка видео по количеству лайков.
        Возвращает URL видео с наибольшим количеством лайков.
        """
        videos = []
        videos_data = self.videos_data_list()

        for video in videos_data['items']:
            video_likes = video['statistics']['likeCount']
            video_id = video['id']
            yt_link = f'https://youtu.be/{video_id}'
            videos.append({'likes': int(video_likes), 'url': yt_link})
        sorted_videos = sorted(videos, key=lambda v: v['likes'], reverse=True)

        return sorted_videos[0]['url']
