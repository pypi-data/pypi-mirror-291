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

import os
import platform

from typing import Union, List, Type

from ..models import Artist, Album, Track, Playlist


def finalizeResponse(response: Union[List[dict], dict], objectType: Type[Union[Artist, Album, Track, Playlist]]) -> Union[List[Union[Artist, Album, Track, Playlist]], dict, None]:
    if not (response or response is False):
        return

    if not isinstance(response, list):
        response = [response]

    for index, obj in enumerate(response):
        if objectType is Playlist:
            playlistType = obj.get("type")

            if playlistType in [0, 5]:
                obj = objectType(obj, False if obj.get("original") else True)

            elif playlistType == 1:
                obj = Album(obj, True)

        else:
            obj = objectType(obj)

        response[index] = obj

    return response if len(response) > 1 else response[0]


def addHTTPsToUrl(url: str) -> str:
    if not ("https://" in url or "http://" in url):
        url = "https://" + url

    return url


def createSearchParams(query: str, limit: int, offset: int) -> dict:
    """Создаёт параметры поискового запроса."""
    return {
        "q": query,
        "count": limit,
        "offset": offset
    }


def fileExistsCaseInsensitive(filename: str) -> Union[str, None]:
    directory, filename = os.path.split(filename)
    if not directory:
        directory = "."

    for root, _, files in os.walk(directory):
        for name in files:
            if name.lower() == filename.lower():
                return os.path.join(root, name)

    return


def checkFile(filename: str) -> Union[str, None]:
    if os.path.isfile(filename):  # Проверка на существование файла в точном регистре
        return filename

    system = platform.system()  # Проверка на операционную систему
    if system not in ["Linux", "Darwin"]:  # Darwin — это macOS
        return

    filename = fileExistsCaseInsensitive(filename)  # Проверка на существование файла без учета регистра
    if not filename:
        return