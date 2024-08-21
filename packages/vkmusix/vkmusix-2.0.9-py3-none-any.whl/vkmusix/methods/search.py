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

from typing import Type, Union, List, Dict

from ..models import Artist, Album, Track, Playlist
from ..utils.another import finalizeResponse, createSearchParams


classes = {Artist: "artists", Album: "albums", Track: "audios", Playlist: "playlists"}


class Search:
    def search(self, query: str, limit: int = 10, offset: int = 0) -> Union[Dict[str, Union[Artist, Album, Track, Playlist]], None, dict]:
        """
        Ищет артистов, альбомы, аудиотреки и плейлисты по запросу.

        Пример использования:\n
        result = client.search(query="prombl", limit=1)\n
        print(result)

        :param query: запрос, по которому осуществить поиск. (str)
        :param limit: максимальное количество объектов каждого типа, которое необходимо вернуть. (int, по умолчанию 10)
        :param offset: количество результатов каждого типа, которые необходимо пропустить. (int, необязательно)
        :return: словарь содержащий один, несколько или все ключи из `artists`, `albums`, `tracks`, `playlists` (если ничего не найдено, то ключ отсутствует), или `None` (если ничего не найдено). Каждый из ключей содержит список объектов этого типа в виде объектов модели или объект этого типа в виде объекта модели (если он единственный).
        """

        return self._searchItems("searchMain", (query, limit, offset), [Artist, Album, Track, Playlist])


    def searchArtists(self, query: str, limit: int = 10, offset: int = 0) -> Union[List[Artist], Artist, None, dict]:
        """
        Ищет артистов по запросу.

        Пример использования:\n
        result = client.searchArtists(query="prombl", limit=1)\n
        print(result)

        :param query: запрос, по которому осуществить поиск. (str)
        :param limit: максимальное количество артистов, которое необходимо вернуть. (int, по умолчанию 10)
        :param offset: количество результатов, которые необходимо пропустить. (int, необязательно)
        :return: список артистов в виде объектов модели `Artist`, артист в виде объекта модели `Artist` (если он единственный) или `None` (если ничего не найдено).
        """

        return self._searchItems("searchArtists", (query, limit, offset), Artist)


    def searchAlbums(self, query: str, limit: int = 10, offset: int = 0) -> Union[List[Album], Album, None, dict]:
        """
        Ищет альбомы по запросу.

        Пример использования:\n
        result = client.searchAlbums(query="prombl — npc", limit=1)\n
        print(result)

        :param query: запрос, по которому осуществить поиск. (str)
        :param limit: максимальное количество альбомов, которое необходимо вернуть. (int, по умолчанию 10)
        :param offset: количество результатов, которые необходимо пропустить. (int, необязательно)
        :return: список альбомов в виде объектов модели `Album`, альбом в виде объекта модели `Album` (если он единственный) или `None` (если ничего не найдено).
        """

        return self._searchItems("searchAlbums", (query, limit, offset), Album)


    def searchTracks(self, query: str, limit: int = 10, offset: int = 0) -> Union[List[Track], Track, None, dict]:
        """
        Ищет аудиотреки по запросу.

        Пример использования:\n
        result = client.searchTracks(query="prombl — zapreti", limit=1)\n
        print(result)

        :param query: запрос, по которому осуществить поиск. (str)
        :param limit: максимальное количество аудиотреков, которое необходимо вернуть. (int, по умолчанию 10)
        :param offset: количество результатов, которые необходимо пропустить. (int, необязательно)
        :return: список аудиотреков в виде объектов модели `Track`, аудиотрек в виде объекта модели `Track` (если он единственный) или `None` (если ничего не найдено).
        """

        return self._searchItems("search", (query, limit, offset), Track)


    def searchPlaylists(self, query: str, limit: int = 10, offset: int = 0) -> Union[List[Playlist], Playlist, None, dict]:
        """
        Ищет плейлисты по запросу.

        Пример использования:\n
        result = client.searchPlaylists(query="Релизы 20.10.2023", limit=1)\n
        print(result)

        :param query: запрос, по которому осуществить поиск. (str)
        :param limit: максимальное количество плейлистов, которое необходимо вернуть. (int, по умолчанию 10)
        :param offset: количество результатов, которые необходимо пропустить. (int, необязательно)
        :return: список плейлистов в виде объектов модели `Playlist`, плейлист в виде объекта модели `Playlist` (если он единственный) или `None` (если ничего не найдено).
        """

        return self._searchItems("searchPlaylists", (query, limit, offset), Playlist)


    def _searchItems(self, method: str, params: tuple, itemClass: Union[List[Type[Union[Artist, Album, Track, Playlist]]], Type[Union[Artist, Album, Track, Playlist]]]) -> Union[List[Union[Artist, Album, Track, Playlist]], Artist, Album, Track, Playlist, None, dict]:
        query, limit, offset = params[0], params[1], params[2]
        if not query:
            return self._raiseError("noneQuery")

        params = createSearchParams(query, limit, offset)
        response = self._VKReq(method, params)

        if isinstance(itemClass, list):
            results = {}
            for model, key in classes.items():
                modelObjects = response.get(key)
                if modelObjects:
                    modelObjects = modelObjects.get("items")

                if not modelObjects:
                    continue

                results[key if key != "audios" else "tracks"] = finalizeResponse(modelObjects, model)

            return results if results else None

        else:
            items = response.get("items")
            return finalizeResponse(items, itemClass)