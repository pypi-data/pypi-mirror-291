#  VKMusix — VK Music API Client Library for Python
#  Copyright (C) 2024—present to4no4sv <https://github.com/to4no4sv/VKMusix>
#
#  This file is part of VKMusix.
#
#  VKMusix is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  VKMusix is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with VKMusix. If not, see <http://www.gnu.org/licenses/>.

import re
import json
import pytz
from datetime import datetime

from .config import VK, moscowTz


def unixToDatetime(seconds: int) -> datetime:
    UTC = datetime.utcfromtimestamp(seconds)
    return UTC.replace(tzinfo=pytz.utc).astimezone(moscowTz)


class _CustomEncoder(json.JSONEncoder):
    def default(self, o) -> any:
        if isinstance(o, _BaseModel):
            return o.toDict()

        elif isinstance(o, datetime):
            return o.strftime("%d/%m/%Y %H:%M:%S")

        elif isinstance(o, type):
            return o.__name__

        return super().default(o)


class _BaseModel:
    def toDict(self) -> any:
        result = {}
        for key, value in self.__dict__.items():
            if value is not None:
                result[key] = value

        return result

    def __repr__(self) -> any:
        return json.dumps(self.toDict(), indent=4, ensure_ascii=False, cls=_CustomEncoder)


class Artist(_BaseModel):
    """
    Класс, представляющий артиста.

    Атрибуты:
        nickname (str): псевдоним артиста.\n
        photo (dict, optional): словарь с размерами и URL фотографий артиста, отсортированный по размеру.\n
        albums (list[Album], optional): список альбомов артиста, представленных объектами класса `Album`.\n
        tracks (list[Track], optional): список аудиотреков артиста, представленных объектами класса `Track`.\n
        id (str): идентификатор артиста.\n
        url (str): URL страницы артиста.
    """

    def __init__(self, artist: dict) -> None:
        self.nickname = artist.get("name")

        photo = artist.get("photo")
        if photo:
            photoDict = {f'{photo.get("width")}': re.sub(r"\.(j|jp|jpg)$", str(), photo.get("url")[:photo.get("url").rfind("&c_uniq_tag=")]) for photo in photo}
            self.photo = dict(sorted(photoDict.items(), key=lambda item: (int(item[0]))))

        else:
            photo = artist.get("photos")
            self.photo = dict(sorted({f'{photo.get("width")}': photo.get("url") for photo in photo[0].get("photo")}.items(), key=lambda item: (int(item[0])))) if photo else None

        albums = artist.get("albums")
        self.albums = [Album(album) for album in albums] if albums else None

        tracks = artist.get("tracks")
        self.tracks = [Track(track) for track in tracks] if tracks else None

        if self.nickname not in ["Various Artists", "Various Artist"]:
            self.id = artist.get("id")
            domain = artist.get("domain")
            self.url = VK + "artist/" + (domain if domain else self.id)

        else:
            self.id = None
            self.url = None


class Album(_BaseModel):
    """
    Класс, представляющий альбом.

    Атрибуты:
        title (str): название альбома.\n
        subtitle (str, optional): подзаголовок альбома, если он присутствует.\n
        description (str, optional): описание альбома, если оно присутствует.\n
        artists (list[Artist]): список основных артистов альбома, представленных объектами класса `Artist`.\n
        featuredArtists (list[Artist], optional): список приглашённых артистов альбома, представленных объектами класса `Artist`.\n
        releaseYear (int, optional): год выпуска альбома.\n
        genres (list[Genre], optional): список жанров альбома, представленных объектами класса Genre.\n
        plays (int, optional): количество прослушиваний альбома.\n
        uploadedAt (datetime, optional): дата и время загрузки альбома (UTC +03:00).\n
        updatedAt (datetime, optional): дата и время последнего обновления информации об альбоме (UTC +03:00).\n
        photo (dict, optional): словарь с размерами и URL фотографий альбома, отсортированный по размеру.\n
        tracks (list[Track], optional): список аудиотреков альбома, где каждый аудиотрек представлен объектом класса `Track`.\n
        exclusive (bool, optional): флаг, указывающий, является ли альбом эксклюзивным.\n
        ownerId (str): идентификатор владельца альбома.\n
        albumId (str): идентификатор альбома.\n
        id (str): комбинированный идентификатор в формате `ownerId_albumId`.\n
        url (str): URL страницы альбома.
    """

    def __init__(self, album: dict, playlist: bool = False) -> None:
        title = album.get("title")
        self.title = title if title else None

        subtitle = album.get("subtitle")
        self.subtitle = subtitle if subtitle else None

        description = album.get("description")
        self.description = description if description else None

        mainArtists = album.get("main_artists")
        self.artists = [Artist(mainArtist) for mainArtist in mainArtists] if mainArtists else None

        featuredArtists = album.get("featured_artists")
        self.featuredArtists = [Artist(featuredArtist) for featuredArtist in featuredArtists] if featuredArtists else None

        releaseYear = album.get("year")
        self.releaseYear = releaseYear if releaseYear else None

        genres = album.get("genres")
        if genres:
            for index, genre in enumerate(genres):
                genres[index] = Genre(genre)
        self.genres = genres if genres else None

        plays = album.get("plays")
        self.plays = plays if plays else None

        uploadedAt = album.get("create_time")
        self.uploadedAt = unixToDatetime(uploadedAt) if uploadedAt else None

        updatedAt = album.get("update_time")
        self.updatedAt = unixToDatetime(updatedAt) if updatedAt else None

        photo = album.get("photo")
        if not photo:
            photo = album.get("thumb")
        self.photo = {key.split("_")[1]: value[:value.rfind("&c_uniq_tag=")] for key, value in photo.items() if key.startswith("photo_")} if photo else None

        original = album.get("original")
        self.original = Album(original) if original else None

        tracks = album.get("tracks")
        self.tracks = tracks if tracks else None

        self.exclusive = album.get("exclusive")

        self.ownerId = album.get("owner_id")
        if not playlist:
            self.albumId = album.get("id") or album.get("playlist_id")
            self.id = f"{self.ownerId}_{self.albumId}"
            self.url = VK + "music/album/" + self.id

        else:
            self.playlistId = album.get("id")
            self.id = f"{self.ownerId}_{self.playlistId}"
            self.url = VK + "music/playlist/" + self.id


class Track(_BaseModel):
    """
    Класс, представляющий аудиотрек.

    Атрибуты:
        title (str): название аудиотрека.\n
        subtitle (str, optional): подзаголовок аудиотрека, если он присутствует.\n
        artists (list[Artist], optional): список основных артистов аудиотрека, представленных объектами класса `Artist`.\n
        artist (str): основной(ые) артист(ы) аудиотрека.\n
        featuredArtists (list[Artist], optional): список приглашённых артистов аудиотрека, представленных объектами класса `Artist`.\n
        genre (Genre, optional): жанр аудиотрека, представленный объектом класса `Genre`.\n
        explicit (bool, optional): флаг, указывающий, есть ли в треке ненормативная лексика.\n
        duration (int): продолжительность аудиотрека в секундах.\n
        fileUrl (str, optional): ссылка на MP3-файл.\n
        lyrics (str, optional): текст аудиотрека.\n
        hasLyrics (bool, optional): флаг, указывающий, имеет ли аудиотрек текст.\n
        uploadedAt (datetime, optional): дата и время загрузки аудиотрека (UTC +03:00).\n
        album (Album, optional): альбом, к которому принадлежит аудиотрек, представленный объектом класса `Album`.\n
        ownerId (str): идентификатор владельца трека.\n
        trackId (str): идентификатор аудиотрека.\n
        id (str): комбинированный идентификатор в формате `ownerId_trackId`.\n
        url (str): URL страницы аудиотрека.
    """

    def __init__(self, track: dict) -> None:
        title = track.get("title")
        self.title = title if title else None

        subtitle = track.get("subtitle")
        self.subtitle = subtitle if subtitle else None

        artist = track.get("artist")
        self.artist = artist if artist else None

        mainArtists = track.get("main_artists")
        self.artists = [Artist(mainArtist) for mainArtist in mainArtists] if mainArtists else None

        featuredArtists = track.get("featured_artists")
        self.featuredArtists = [Artist(featuredArtist) for featuredArtist in featuredArtists] if featuredArtists else None

        genreId = track.get("genre_id")
        self.genre = Genre(genreId=genreId) if genreId else None

        self.explicit = track.get("is_excplicit")

        duration = track.get("duration")
        self.duration = duration if duration else None

        fileUrl = track.get("url")
        self.fileUrl = fileUrl[:fileUrl.rfind("?siren=1")] if fileUrl else None

        lyrics = track.get("lyrics")
        self.lyrics = lyrics if lyrics else None
        self.hasLyrics = track.get("has_lyrics") if not lyrics else None

        uploadedAt = track.get("date")
        self.uploadedAt = unixToDatetime(uploadedAt) if uploadedAt else None

        album = track.get("album")
        self.album = Album(album) if album else None

        self.licensed = track.get("is_licensed")

        self.ownerId = track.get("owner_id")
        self.trackId = track.get("id")
        self.id = f"{self.ownerId}_{self.trackId}"

        releaseAudioId = track.get("release_audio_id")
        self.url = VK + "audio" + (self.id if not releaseAudioId else releaseAudioId)


class Playlist(_BaseModel):
    """
    Класс, представляющий плейлист.

    Атрибуты:
        title (str): название плейлиста.\n
        subtitle (str, optional): подзаголовок плейлиста, если он присутствует.\n
        description (str, optional): описание плейлиста, если оно присутствует.\n
        plays (int, optional): количество прослушиваний плейлиста.\n
        createdAt (datetime, optional): дата и время создания плейлиста (UTC +03:00).\n
        updatedAt (datetime, optional): дата и время последнего добавления (удаления) аудиотрека в (из) плейлист(а) (UTC +03:00).\n
        photo (dict, optional): словарь с размерами и URL фотографий плейлиста, отсортированный по размеру.\n
        tracks (list[Track], optional): список аудиотреков плейлиста, где каждый аудиотрек представлен объектом класса `Track`.\n
        ownerId (str): идентификатор владельца плейлиста.\n
        playlistId (str): идентификатор плейлиста.\n
        id (str): комбинированный идентификатор в формате `ownerId_playlistId`.\n
        url (str): URL страницы плейлиста.
    """

    def __init__(self, playlist: dict, isOwn: bool = False) -> None:
        title = playlist.get("title")
        self.title = title if title else None

        subtitle = playlist.get("subtitle")
        self.subtitle = subtitle if subtitle else None

        description = playlist.get("description")
        self.description = description if description else None

        plays = playlist.get("plays")
        self.plays = plays if plays else None

        createddAt = playlist.get("create_time")
        self.createdAt = unixToDatetime(createddAt) if createddAt else None

        updatedAt = playlist.get("update_time")
        self.updatedAt = unixToDatetime(updatedAt) if updatedAt else None

        photo = playlist.get("photo")
        if not photo:
            photo = playlist.get("thumb")
        self.photo = {key.split("_")[1]: value[:value.rfind("&c_uniq_tag=")] for key, value in photo.items() if key.startswith("photo_")} if photo else None

        original = playlist.get("original")
        self.original = Playlist(original) if original else None

        tracks = playlist.get("tracks")
        self.tracks = tracks if tracks else None

        self.ownerId = playlist.get("owner_id")
        self.playlistId = playlist.get("id") or playlist.get("playlist_id")
        self.id = f"{self.ownerId}_{self.playlistId}"
        self.url = VK + "music/playlist/" + self.id

        self.own = isOwn


trackGenres = {
    1: "Рок",
    2: "Поп",
    3: "Рэп и Хип-хоп",
    4: "Расслабляющая",
    5: "House и Танцевальная",
    6: "Инструментальная",
    7: "Метал",
    8: "Дабстеп",
    10: "Drum & Bass",
    11: "Транс",
    12: "Шансон",
    13: "Этническая",
    14: "Акустическая",
    15: "Регги",
    16: "Классическая",
    17: "Инди-поп",
    18: "Другая",
    19: "Скит",
    21: "Альтернатива",
    22: "Электро-поп и Диско",
    1001: "Джаз и Блюз"
}


class Genre(_BaseModel):
    """
    Класс, представляющий жанр аудиотрека или альбома.

    Атрибуты:
        title (str): название жанра.\n
        id (str): идентификатор жанра.\n
    """

    def __init__(self, genre: dict = None, genreId: int = None) -> None:
        if genreId:
            self.title = trackGenres.get(genreId, "Неизвестен")

            self.id = genreId

        else:
            self.title = genre.get("name")

            self.id = genre.get("id")