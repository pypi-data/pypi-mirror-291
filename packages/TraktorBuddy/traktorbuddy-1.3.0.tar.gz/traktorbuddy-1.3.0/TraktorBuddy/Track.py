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

import os
import xml.etree.ElementTree as ET
import PIL.Image  # type: ignore

from datetime import datetime
from io import BytesIO
from mutagen import File as MutagenFile  # type: ignore
from typing import Optional, BinaryIO
from enum import IntEnum, unique

from .Utility import Utility
from .Key import OpenNotation
from .Rating import Rating
from .Color import Color


# -- Class
class Track:
    """Interface for Traktor tracks."""

    @unique
    class Filter(IntEnum):
        ONLY_TRACKS = 1
        ONLY_STEMS = 2

    def __init__(self, entry_element: ET.Element):
        """Constructor from an XML entry element."""

        self._entry_element: ET.Element = entry_element
        self._info_element: Optional[ET.Element] = self._entry_element.find('INFO')
        self._album_element: Optional[ET.Element] = self._entry_element.find('ALBUM')

    def _entryElement(self) -> ET.Element:
        return self._entry_element

    def _getInfoElement(self) -> ET.Element:
        if self._info_element is None:
            self._info_element = ET.SubElement(self._entry_element, 'INFO')

            if self._info_element is None:
                raise RuntimeError('Error creating track INFO element.')

        return self._info_element

    def _getAlbumElement(self) -> ET.Element:
        if self._album_element is None:
            self._album_element = ET.SubElement(self._entry_element, 'ALBUM')

            if self._album_element is None:
                raise RuntimeError('Error creating track ALBUM element.')

        return self._album_element

    def _markAsModifiedNow(self) -> None:
        date: datetime = Utility.utcTimeNow()

        self._entry_element.set('MODIFIED_DATE', date.strftime('%Y/%m/%d'))
        self._entry_element.set('MODIFIED_TIME', str(date.second + (date.minute * 60) + (date.hour * 3600)))

    def _playlistKey(self) -> Optional[str]:
        location = self._entry_element.find('LOCATION')
        if location is None:
            return None

        webaddress = location.get('WEBADDRESS')
        if webaddress is not None:
            return webaddress

        volume = location.get('VOLUME')
        if volume is None:
            return None

        directory = location.get('DIR')
        if directory is None:
            return None

        file = location.get('FILE')
        if file is None:
            return None

        return volume + directory + file

    def getFromEntryElement(self, name: str) -> Optional[ET.Element]:
        return self._entry_element.find(name)

    def setInEntryElement(self, name: str, value: str, mark_as_modified: bool = True) -> None:
        self._entry_element.set(name, value)

        if mark_as_modified is True:
            self._markAsModifiedNow()

    def removeFromEntryElement(self, name: str, mark_as_modified: bool = True) -> None:
        element = self._entry_element.find(name)
        if element is None:
            return

        self._entry_element.remove(element)

        if mark_as_modified is True:
            self._markAsModifiedNow()

    def getFromAlbumElement(self, name: str) -> Optional[str]:
        if self._album_element is None:
            return None

        return self._album_element.get(name)

    def setInAlbumElement(self, name: str, value: Optional[str], mark_as_modified: bool = True) -> None:
        if self._album_element is None:
            if value is None:
                return

            self._album_element = ET.SubElement(self._entry_element, 'ALBUM')

        if value is None:
            self._album_element.attrib.pop(name)
        else:
            self._album_element.set(name, value)

        if mark_as_modified is True:
            self._markAsModifiedNow()

    def getFromInfoElement(self, name: str) -> Optional[str]:
        if self._info_element is None:
            return None

        return self._info_element.get(name)

    def setInInfoElement(self, name: str, value: Optional[str], mark_as_modified: bool = True) -> None:
        if self._info_element is None:
            if value is None:
                return

            self._info_element = ET.SubElement(self._entry_element, 'INFO')

        if value is None:
            self._info_element.attrib.pop(name)
        else:
            self._info_element.set(name, value)

        if mark_as_modified is True:
            self._markAsModifiedNow()

    def flags(self) -> int:
        flags_value: Optional[str] = self.getFromInfoElement('FLAGS')
        return int(flags_value if flags_value is not None else 0)

    def setFlags(self, flags: int, mark_as_modified: bool = True) -> None:
        self.setInInfoElement('FLAGS', str(flags))

        if mark_as_modified is True:
            self._markAsModifiedNow()

    def matchesFilter(self, filter: int) -> bool:
        if filter == 0:
            return True
        elif filter == Track.Filter.ONLY_TRACKS:
            return not self.isAStem() and not self.isASample()
        elif filter == Track.Filter.ONLY_STEMS:
            return self.isAStem()
        else:
            return False

    def hasStemsVersionGenerated(self) -> bool:
        return (self.flags() & 0x40) != 0

    def isASample(self) -> bool:
        return self._entry_element.find('LOOPINFO') is not None

    def isAStem(self) -> bool:
        return self.hasStemsVersionGenerated() or self._entry_element.find('STEMS') is not None

    def location(self) -> Optional[str]:
        playlist_key: Optional[str] = self._playlistKey()
        if playlist_key is None:
            return None

        if playlist_key.startswith('beatport:'):
            return playlist_key

        return '/Volumes/' + playlist_key.replace('/:', '/')

    def modificationDate(self) -> Optional[datetime]:
        modified_date: Optional[str] = self._entry_element.get('MODIFIED_DATE')
        if modified_date is None:
            return None
        date: Optional[datetime] = Utility.dateFromString(modified_date, '%Y/%m/%d')
        if date is None:
            return None

        modified_time: Optional[str] = self._entry_element.get('MODIFIED_TIME')
        if modified_time is None:
            return None
        seconds: Optional[int] = Utility.stringToInt(modified_time)
        if seconds is None:
            return date

        seconds = seconds % (24 * 3600)
        hour: int = seconds // 3600
        seconds %= 3600
        minutes: int = seconds // 60
        seconds %= 60

        # -- Traktor modification dates are stored in UTC time.
        return Utility.utcDatetime(date.year, date.month, date.day, hour, minutes, seconds)

    def title(self) -> Optional[str]:
        return self._entry_element.get('TITLE')

    def setTitle(self, value: str, mark_as_modified: bool = True) -> None:
        self.setInEntryElement('TITLE', value, mark_as_modified)

    def artist(self) -> Optional[str]:
        return self._entry_element.get('ARTIST')

    def setArtist(self, value: str, mark_as_modified: bool = True) -> None:
        self.setInEntryElement('ARTIST', value, mark_as_modified)

    def beatgridLocked(self) -> bool:
        return self._entry_element.get('LOCK') == '1'

    def setBeatGridLocked(self, value: bool, mark_as_modified: bool = True) -> None:
        string: str = '1' if value is True else '0'

        self.setInEntryElement('LOCK', string, mark_as_modified)

        if mark_as_modified is True:
            self._markAsModifiedNow()

            date: datetime = Utility.utcTimeNow()
            self._entry_element.set('LOCK_MODIFICATION_TIME', date.strftime('%Y-%m-%dT%H:%M:%S'))

    def beatgridLockModifiedDate(self) -> Optional[datetime]:
        string: Optional[str] = self._entry_element.get('LOCK_MODIFICATION_TIME')
        if string is None:
            return None

        return Utility.dateFromString(string, '%Y-%m-%dT%H:%M:%S', utc=True)

    def bitrate(self) -> Optional[int]:
        return Utility.stringToInt(self.getFromInfoElement('BITRATE'))

    def setBitrate(self, value: int, mark_as_modified: bool = True) -> None:
        self.setInInfoElement('BITRATE', str(value), mark_as_modified)

    def genre(self) -> Optional[str]:
        return self.getFromInfoElement('GENRE')

    def setGenre(self, value: str, mark_as_modified: bool = True) -> None:
        self.setInInfoElement('GENRE', value, mark_as_modified)

    def label(self) -> Optional[str]:
        return self.getFromInfoElement('LABEL')

    def setLabel(self, value: str, mark_as_modified: bool = True) -> None:
        self.setInInfoElement('LABEL', value, mark_as_modified)

    def producer(self) -> Optional[str]:
        return self.getFromInfoElement('PRODUCER')

    def setProducer(self, value: str, mark_as_modified: bool = True) -> None:
        self.setInInfoElement('PRODUCER', value, mark_as_modified)

    def mix(self) -> Optional[str]:
        return self.getFromInfoElement('MIX')

    def setMix(self, value: str, mark_as_modified: bool = True) -> None:
        self.setInInfoElement('MIX', value, mark_as_modified)

    def release(self) -> Optional[str]:
        return self.getFromAlbumElement('TITLE')

    def setRelease(self, value: str, mark_as_modified: bool = True) -> None:
        self.setInAlbumElement('TITLE', value, mark_as_modified)

    def trackNumber(self) -> Optional[int]:
        return Utility.stringToInt(self.getFromAlbumElement('TRACK'))

    def setTrackNumber(self, value: int, mark_as_modified: bool = True) -> None:
        self.setInAlbumElement('TRACK', str(value), mark_as_modified)

    def comments(self) -> Optional[str]:
        return self.getFromInfoElement('COMMENT')

    def setComments(self, value: str, mark_as_modified: bool = True) -> None:
        self.setInInfoElement('COMMENT', value, mark_as_modified)

    def comments2(self) -> Optional[str]:
        return self.getFromInfoElement('RATING')

    def setComments2(self, value: str, mark_as_modified: bool = True) -> None:
        self.setInInfoElement('RATING', value, mark_as_modified)

    def remixer(self) -> Optional[str]:
        return self.getFromInfoElement('REMIXER')

    def setRemixer(self, value: str, mark_as_modified: bool = True) -> None:
        self.setInInfoElement('REMIXER', value, mark_as_modified)

    def key(self) -> Optional[str]:
        return self.getFromInfoElement('KEY')

    def setKey(self, value: str, mark_as_modified: bool = True) -> None:
        self.setInInfoElement('KEY', value, mark_as_modified)

    def playCount(self) -> Optional[int]:
        return Utility.stringToInt(self.getFromInfoElement('PLAYCOUNT'))

    def setPlayCount(self, value: int, mark_as_modified: bool = True) -> None:
        self.setInInfoElement('PLAYCOUNT', str(value), mark_as_modified)

    def length(self) -> Optional[float]:
        return Utility.stringToFloat(self.getFromInfoElement('PLAYTIME_FLOAT'))

    def setLength(self, value: float, mark_as_modified: bool = True) -> None:
        self.setInInfoElement('PLAYTIME', str(round(value)), mark_as_modified=False)
        self.setInInfoElement('PLAYTIME_FLOAT', '{:.06f}'.format(value), mark_as_modified)

    def rating(self) -> Optional[Rating]:
        # -- The following works with rekordbox and Serato too:
        # --    Unrated -> 0, 1-51 -> 1, 52-102 -> 2, 103-153 -> 3, 154-204 -> 4, 205-anything -> 5
        value: Optional[int] = Utility.stringToInt(self.getFromInfoElement('RANKING'))

        if value is None:
            return None

        if value == 0:
            return Rating.Unrated
        elif value < 52:
            return Rating.OneStar
        elif value < 103:
            return Rating.TwoStars
        elif value < 154:
            return Rating.ThreeStars
        elif value < 205:
            return Rating.FourStars
        elif value <= 255:
            return Rating.FiveStars

        return None

    def setRating(self, value: Rating, mark_as_modified: bool = True) -> None:
        map = {
            Rating.Unrated: 0,
            Rating.OneStar: 51,
            Rating.TwoStars: 102,
            Rating.ThreeStars: 153,
            Rating.FourStars: 205,
            Rating.FiveStars: 255
        }

        self.setInInfoElement('RANKING', str(map[value]), mark_as_modified)

    def importDate(self) -> Optional[datetime]:
        return Utility.dateFromString(self.getFromInfoElement('IMPORT_DATE'), '%Y/%m/%d')

    def setImportDate(self, value: datetime, mark_as_modified: bool = True) -> None:
        self.setInInfoElement('IMPORT_DATE', value.strftime('%Y/%m/%d'), mark_as_modified)

    def lastPlayedDate(self) -> Optional[datetime]:
        return Utility.dateFromString(self.getFromInfoElement('LAST_PLAYED'), '%Y/%m/%d')

    def setLastPlayedDate(self, value: datetime, mark_as_modified: bool = True) -> None:
        self.setInInfoElement('LAST_PLAYED', value.strftime('%Y/%m/%d'), mark_as_modified)

    def releaseDate(self) -> Optional[datetime]:
        return Utility.dateFromString(self.getFromInfoElement('RELEASE_DATE'), '%Y/%m/%d')

    def setReleaseDate(self, value: datetime, mark_as_modified: bool = True) -> None:
        self.setInInfoElement('RELEASE_DATE', value.strftime('%Y/%m/%d'), mark_as_modified)

    def fileSize(self) -> Optional[int]:
        return Utility.stringToInt(self.getFromInfoElement('FILESIZE'))

    def setFileSize(self, value: int, mark_as_modified: bool = True) -> None:
        self.setInInfoElement('FILESIZE', str(value), mark_as_modified)

    def bpm(self) -> Optional[float]:
        tempo_element: Optional[ET.Element] = self._entry_element.find('TEMPO')
        if tempo_element is None:
            return None

        return Utility.stringToFloat(tempo_element.get('BPM'))

    def setBpm(self, value: float, mark_as_modified: bool = True) -> None:
        tempo_element: Optional[ET.Element] = self._entry_element.find('TEMPO')
        if tempo_element is None:
            tempo_element = ET.SubElement(self._entry_element, 'TEMPO')

        tempo_element.set('BPM', '{:.06f}'.format(value))
        tempo_element.set('BPM_QUALITY', '100.000000')

        if mark_as_modified is True:
            self._markAsModifiedNow()

    def traktorKey(self) -> Optional[OpenNotation]:
        key_element: Optional[ET.Element] = self._entry_element.find('MUSICAL_KEY')
        if key_element is None:
            return None

        value: Optional[int] = Utility.stringToInt(key_element.get('VALUE'))
        if value is None:
            return None

        result: Optional[OpenNotation] = None

        try:
            result = OpenNotation(value)
        except ValueError:
            pass

        return result

    def setTraktorKey(self, value: OpenNotation, mark_as_modified: bool = True) -> None:
        key_element: Optional[ET.Element] = self._entry_element.find('MUSICAL_KEY')
        if key_element is None:
            key_element = ET.SubElement(self._entry_element, 'MUSICAL_KEY')

        key_element.set('VALUE', str(int(value)))

        if mark_as_modified is True:
            self._markAsModifiedNow()

    def color(self) -> Optional[Color]:
        value: Optional[int] = Utility.stringToInt(self.getFromInfoElement('COLOR'))
        if value is None:
            return None

        result: Optional[Color] = None

        try:
            result = Color(value)
        except ValueError:
            pass

        return result

    def setColor(self, value: Color, mark_as_modified: bool = True) -> None:
        self.setInInfoElement('COLOR', str(int(value)), mark_as_modified)

    def coverArtImageFromFile(self) -> Optional[PIL.Image.Image]:
        track_file_path: Optional[str] = self.location()
        if track_file_path is None or not os.path.exists(track_file_path):
            return None

        try:
            # -- Mutagen can automatically detect format and type of tags
            file: MutagenFile = MutagenFile(track_file_path)

            # -- Access APIC frame and grab the image
            tag = file.tags.get('APIC:', None)

            artwork_data: Optional[BytesIO] = None
            if tag is not None:
                artwork_data = BytesIO(tag.data)
            else:
                cover_list = file.get('covr', None)
                if cover_list is not None and len(cover_list) != 0:
                    # -- We only use the first cover from the list
                    artwork_data = BytesIO(cover_list[0])

            if artwork_data is None:
                return None

            return PIL.Image.open(artwork_data)
        except Exception:
            pass

        return None

    def coverArtCacheFile(self, collection_folder_path: str) -> Optional[str]:
        cover_art_id: Optional[str] = self.getFromInfoElement('COVERARTID')
        if cover_art_id is None:
            return None

        return os.path.join(collection_folder_path, 'CoverArt', cover_art_id) + '000'

    def coverArtImageFromCache(self, collection_folder_path: str) -> Optional[PIL.Image.Image]:
        database_image_path: Optional[str] = self.coverArtCacheFile(collection_folder_path)
        if database_image_path is None or not os.path.exists(database_image_path):
            return None

        artwork_file: BinaryIO = open(database_image_path, "rb")
        data = artwork_file.read()
        artwork_file.close()

        if data[0] != 8:
            return None

        width: int = ((data[4] << 24) | (data[3] << 16) | (data[2] << 8) | data[1])
        height: int = ((data[8] << 24) | (data[7] << 16) | (data[6] << 8) | data[5])
        rgba_data: bytearray = bytearray()

        # -- Re-order the color components from little endian data.
        for pixel_index in range(0, width * height):
            data_index: int = 9 + (pixel_index * 4)

            rgba_data.append(data[data_index + 2])
            rgba_data.append(data[data_index + 1])
            rgba_data.append(data[data_index])
            rgba_data.append(data[data_index + 3])

        return PIL.Image.frombytes('RGBA', (width, height), bytes(rgba_data))
