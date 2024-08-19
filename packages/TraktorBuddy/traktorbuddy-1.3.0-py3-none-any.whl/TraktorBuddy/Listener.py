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

from traktor_nowplaying import Listener as TraktorListener  # type: ignore
from typing import Callable, Dict, Optional

from .Collection import Collection
from .Track import Track
from .FakeTrack import FakeTrack


# -- Class
class Listener:
    """Interface for listening to what Traktor is playing."""

    def __init__(self, collection: Collection, callback: Callable[[Track], None]):
        """Constructor a Traktor collection and a method to call when new tracks are posted."""

        self._collection: Collection = collection
        self._listener: TraktorListener = TraktorListener(port=8000, quiet=True, custom_callback=self._new_track_callback)
        self._track_key_to_index: Dict[str, int] = {}
        self._callback: Callable[[Track], None] = callback

        # -- Build our track name-artist to index map
        for index in range(self._collection.numberOfTracks()):
            track: Track = self._collection.trackAtIndex(index)

            title: Optional[str] = track.title()
            if title is None:
                continue

            artist: Optional[str] = track.artist()
            if artist is None:
                continue

            key: str = f'{title}{artist}'
            if key not in self._track_key_to_index:
                self._track_key_to_index[key] = index

    def _new_track_callback(self, data) -> None:
        info: Dict[str, str] = dict(data)
        title: str = info.get('title', '')
        artist: str = info.get('artist', '')

        if len(title) == 0 or len(artist) == 0:
            return

        track_string: str = f'{title}{artist}'
        track_index: Optional[int] = self._track_key_to_index.get(track_string, None)
        if track_index is not None:
            self._callback(self._collection.trackAtIndex(track_index))
        else:
            self._callback(FakeTrack(title, artist))

    def start(self) -> None:
        self._listener.start()
