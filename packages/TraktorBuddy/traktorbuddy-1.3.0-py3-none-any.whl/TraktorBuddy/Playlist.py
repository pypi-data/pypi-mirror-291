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

import xml.etree.ElementTree as ET

from typing import List, Optional

from .Track import Track
from .TrackList import TrackList


# -- Class
class Playlist:
    """Interface for Traktor playlists."""

    def __init__(self, track_list: TrackList, node_element: ET.Element):
        """Constructor from an XML entry element."""

        self._node_element: ET.Element = node_element
        self._track_list: TrackList = track_list
        self._tracks: Optional[List[Track]] = None

    def name(self) -> Optional[str]:
        return self._node_element.get('NAME')

    def tracks(self, filter: int = 0) -> List[Track]:
        if self._tracks is not None:
            if filter == 0:
                return self._tracks

            result: List[Track] = []

            for track in self._tracks:
                if track.matchesFilter(filter):
                    result.append(track)

            return result

        self._tracks = []

        playlist_element: Optional[ET.Element] = self._node_element.find('PLAYLIST')
        if playlist_element is None:
            return self._tracks

        if playlist_element.get('TYPE') != 'LIST':
            return self._tracks

        for entry in playlist_element.findall('ENTRY'):
            primary_key: Optional[ET.Element] = entry.find('PRIMARYKEY')
            if primary_key is None:
                continue

            type: Optional[str] = primary_key.get('TYPE')
            if type != 'TRACK' and type != 'STEM':
                continue

            key: Optional[str] = primary_key.get('KEY')
            if key is None:
                continue

            track_found: Optional[Track] = self._track_list.trackWithPlaylistKey(key)
            if track_found is None:
                continue

            if filter != 0 and not track_found.matchesFilter(filter):
                continue

            self._tracks.append(track_found)

        return self._tracks
