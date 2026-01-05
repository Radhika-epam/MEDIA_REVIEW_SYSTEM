from models.media import Movie, WebShow, Song

class MediaFactory:
    @staticmethod
    def create_media(media_type, title):
        if media_type == "movie":
            return Movie(title)
        elif media_type == "webshow":
            return WebShow(title)
        elif media_type == "song":
            return Song(title)
        else:
            raise ValueError("Invalid media type")
