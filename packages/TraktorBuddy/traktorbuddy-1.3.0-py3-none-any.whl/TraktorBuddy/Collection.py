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

from typing import List, Optional
from semver import VersionInfo
from time import sleep
from pathlib import Path

from .Utility import Utility
from .Track import Track
from .TrackList import TrackList
from .Folder import Folder
from .Playlist import Playlist
from .Exceptions import ArgumentError


# -- Classes
class Collection:
    """Interface for Traktor collection."""

    def __init__(self, collection_path: Optional[str] = None, _mock_element: Optional[ET.Element] = None):
        """Constructor from a collection path, or it will just use the latest collection if no path is provided."""

        self._nml_element: Optional[ET.Element] = None
        self._collection_path: Optional[str] = None
        self._collection_folder_path: Optional[str] = None

        if _mock_element is None:
            if collection_path is None:
                self._collection_path = Collection.traktorCollectionFilePath()

                if self._collection_path is None:
                    raise RuntimeError('Error: Could not find any Traktor folder in \'' + Collection.nativeInstrumentsFolderPath() + '\'.')
            else:
                self._collection_path = collection_path

            self._collection_folder_path = str(Path(self._collection_path).parent)

            print('Parsing Traktor collection in \'' + self._collection_path + '\'.')

            self._nml_element = ET.ElementTree(file=self._collection_path).getroot()
        else:
            self._nml_element = _mock_element

        collection_element: Optional[ET.Element] = self._nml_element.find('COLLECTION')
        if collection_element is None:
            raise RuntimeError('Error: Could not find COLLECTION element in Traktor collection file.')

        self._track_list: TrackList = TrackList(collection_element)

    def folderPath(self) -> Optional[str]:
        return self._collection_folder_path

    def makeBackup(self) -> None:
        # -- Backups filename have a timestamp so we make sure to wait so that names cannot clash.
        sleep(1)

        backup_folder: Optional[str] = Collection.traktorCollectionBackupFolderPath()
        if backup_folder is None:
            return

        os.makedirs(backup_folder, exist_ok=True)

        if self._collection_path is None:
            raise RuntimeError('Error: No collection path set.')

        arguments: List[str] = ['zip', '-j', Utility.utcTimeNow().strftime('%Y-%m-%d-%H-%M-%S.zip'), self._collection_path]
        Utility.shellCommand(arguments, backup_folder)

    def save(self):
        self.makeBackup()

        if self._collection_path is None or self._nml_element is None:
            raise RuntimeError('Error: Invalid collection object.')

        with open(self._collection_path, 'w') as out_file:
            out_file.write(Utility.xmlElementToString(self._nml_element, xml_declaration=True))

        print('Saved Traktor collection in \'' + self._collection_path + '\'.')

    def findAllTracksAtPath(self, path: str, filter: int = 0) -> List[Track]:
        root_folder: Optional[Folder] = self.rootFolder()
        if root_folder is None:
            return []

        if path == '' or path == '/':
            return self.tracks(filter)

        crate: Optional[Folder | Playlist] = root_folder.find(path.split('/'))
        if crate is None:
            raise RuntimeError('Could not find any folder or playlist at \'' + path + '\'.')
        else:
            return crate.tracks(filter)

    def tracks(self, filter: int = 0) -> List[Track]:
        return self._track_list.tracks(filter)

    def numberOfTracks(self) -> int:
        return len(self._track_list.tracks())

    def trackAtIndex(self, index: int) -> Track:
        if index >= self.numberOfTracks():
            raise ArgumentError("Out of bound access to a track.")

        return self._track_list.tracks()[index]

    def rootFolder(self) -> Optional[Folder]:
        nml_element: Optional[ET.Element] = self._nml_element
        if nml_element is None:
            raise RuntimeError('Error: Invalid collection object.')

        playlists_element: Optional[ET.Element] = nml_element.find('PLAYLISTS')
        if playlists_element is None:
            return None

        root_node: Optional[ET.Element] = playlists_element.find('NODE')
        if root_node is None:
            return None

        return Folder(self._track_list, root_node)

    def trackWithPlaylistKey(self, key) -> Optional[Track]:
        return self._track_list.trackWithPlaylistKey(key)

    @classmethod
    def purgeBackups(cls, test_mode: bool = False):
        backup_folder: Optional[str] = Collection.traktorCollectionBackupFolderPath()
        if backup_folder is None:
            return

        backup_list: List[str] = os.listdir(backup_folder)
        nb_of_backups: int = len(backup_list)
        if nb_of_backups < 2:
            print('No backups to purge.')
            return

        if test_mode is False:
            backup_list.sort()

            for file in backup_list[:-1]:
                os.remove(os.path.join(backup_folder, file))

        print('Purged ' + str(nb_of_backups - 1) + ' backup(s).')

    @classmethod
    def traktorCollectionBackupFolderPath(cls) -> Optional[str]:
        traktor_folder_path: Optional[str] = Collection.latestTraktorFolderPath()
        if traktor_folder_path is None:
            return None

        return os.path.join(traktor_folder_path, 'Backup', 'TraktorBuddy')

    @classmethod
    def nativeInstrumentsFolderPath(cls) -> str:
        return os.path.join(os.path.expanduser('~'), 'Documents', 'Native Instruments')

    @classmethod
    def latestTraktorFolderPath(cls) -> Optional[str]:
        base_folder: str = Collection.nativeInstrumentsFolderPath()

        lastest_version: Optional[VersionInfo] = None

        for path in os.listdir(base_folder):
            if not path.startswith('Traktor '):
                continue

            try:
                version: Optional[VersionInfo] = VersionInfo.parse(path[8:])

                if version is not None:
                    if lastest_version is None or version > lastest_version:
                        lastest_version = version
            except ValueError:
                continue

        if lastest_version is None:
            return None

        return os.path.join(base_folder, 'Traktor ' + str(lastest_version))

    @classmethod
    def traktorCollectionFilePath(cls) -> Optional[str]:
        traktor_folder_path: Optional[str] = Collection.latestTraktorFolderPath()
        if traktor_folder_path is None:
            return None

        return os.path.join(traktor_folder_path, 'collection.nml')
