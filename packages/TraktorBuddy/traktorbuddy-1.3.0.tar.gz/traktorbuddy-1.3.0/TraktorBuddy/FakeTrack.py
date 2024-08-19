#
# Copyright (c) 2022-present Didier Malenfant <didier@malenfant.net>
#
# This file is part of TraktorBuddy.
#
# TraktorBuddy is free software: you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TraktorBuddy is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU General Public License along with TraktorBuddy. If not,
# see <https://www.gnu.org/licenses/>.
#

import PIL.Image  # type: ignore

from datetime import datetime
from typing import Optional

from .Key import OpenNotation
from .Rating import Rating
from .Color import Color
from .Track import Track


# -- Class
class FakeTrack(Track):
    """Interface for a Fake Traktor track used by the Listener."""

    def __init__(self, title: str, artist: str):
        """Constructor from a title and an artist."""

        self._title: str = title
        self._artist: str = artist

    def _markAsModifiedNow(self) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def hasStemsVersionGenerated(self) -> bool:
        return False

    def isASample(self) -> bool:
        return False

    def isAStem(self) -> bool:
        return False

    def matchesFilter(self, filter: int) -> bool:
        return False

    def location(self) -> Optional[str]:
        return None

    def modificationDate(self) -> Optional[datetime]:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def title(self) -> Optional[str]:
        return self._title

    def setTitle(self, value: str, mark_as_modified: bool = True) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def artist(self) -> Optional[str]:
        return self._artist

    def setArtist(self, value: str, mark_as_modified: bool = True) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def beatgridLocked(self) -> bool:
        return False

    def setBeatGridLocked(self, value: bool, mark_as_modified: bool = True) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def beatgridLockModifiedDate(self) -> Optional[datetime]:
        return None

    def bitrate(self) -> Optional[int]:
        return None

    def setBitrate(self, value: int, mark_as_modified: bool = True) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def genre(self) -> Optional[str]:
        return None

    def setGenre(self, value: str, mark_as_modified: bool = True) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def label(self) -> Optional[str]:
        return None

    def setLabel(self, value: str, mark_as_modified: bool = True) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def producer(self) -> Optional[str]:
        return None

    def setProducer(self, value: str, mark_as_modified: bool = True) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def mix(self) -> Optional[str]:
        return None

    def setMix(self, value: str, mark_as_modified: bool = True) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def release(self) -> Optional[str]:
        return None

    def setRelease(self, value: str, mark_as_modified: bool = True) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def trackNumber(self) -> Optional[int]:
        return None

    def setTrackNumber(self, value: int, mark_as_modified: bool = True) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def comments(self) -> Optional[str]:
        return None

    def setComments(self, value: str, mark_as_modified: bool = True) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def comments2(self) -> Optional[str]:
        return ''

    def setComments2(self, value: str, mark_as_modified: bool = True) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def remixer(self) -> Optional[str]:
        return None

    def setRemixer(self, value: str, mark_as_modified: bool = True) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def key(self) -> Optional[str]:
        return None

    def setKey(self, value: str, mark_as_modified: bool = True) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def playCount(self) -> Optional[int]:
        return None

    def setPlayCount(self, value: int, mark_as_modified: bool = True) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def length(self) -> Optional[float]:
        return None

    def setLength(self, value: float, mark_as_modified: bool = True) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def rating(self) -> Optional[Rating]:
        return None

    def setRating(self, value: Rating, mark_as_modified: bool = True) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def importDate(self) -> Optional[datetime]:
        return None

    def setImportDate(self, value: datetime, mark_as_modified: bool = True) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def lastPlayedDate(self) -> Optional[datetime]:
        return None

    def setLastPlayedDate(self, value: datetime, mark_as_modified: bool = True) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def releaseDate(self) -> Optional[datetime]:
        return None

    def setReleaseDate(self, value: datetime, mark_as_modified: bool = True) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def fileSize(self) -> Optional[int]:
        return None

    def setFileSize(self, value: int, mark_as_modified: bool = True) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def bpm(self) -> Optional[float]:
        return None

    def setBpm(self, value: float, mark_as_modified: bool = True) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def traktorKey(self) -> Optional[OpenNotation]:
        return None

    def setTraktorKey(self, value: OpenNotation, mark_as_modified: bool = True) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def color(self) -> Optional[Color]:
        return None

    def setColor(self, value: Color, mark_as_modified: bool = True) -> None:
        raise RuntimeError('Illegal call on a FakeTrack.')

    def coverArtImageFromFile(self) -> Optional[PIL.Image.Image]:
        return None

    def coverArtCacheFile(self, collection_folder_path: str) -> Optional[str]:
        return None

    def coverArtImageFromCache(self, collection_folder_path: str) -> Optional[PIL.Image.Image]:
        return None
