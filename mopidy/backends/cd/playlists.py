from __future__ import unicode_literals

import glob
import logging
import os
import shutil

from mopidy import settings
from mopidy.backends import base, listener
from mopidy.models import Playlist
from mopidy.utils import formatting

logger = logging.getLogger('mopidy.backends.cd')


class CdPlaylistsProvider(base.BasePlaylistsProvider):
    def __init__(self, *args, **kwargs):
        super(CdPlaylistsProvider, self).__init__(*args, **kwargs)
        self._path = settings.CD_DEVICE_PATH
        self._playlists={}
        self.refresh()

    @property
    def playlists(self):
        logger.info('Returning playlists %s'%self._playlists.values())
        return self._playlists.values()

    def create(self, name):
        pass

    def delete(self, uri):
        pass

    def lookup(self, uri):
        logger.info('Returning playlist %s'%self._playlists[uri])
        return self._playlists[uri]

    def refresh(self):
        logger.info('Loading cd playlist')
        if self.backend.library._album is None:
            return
        album=self.backend.library._album
        tracks=self.backend.library._tracks
        if len(album.artists)>1:
            artistname='Various Artists'
        else:
            artistname=list(album.artists)[0].name
        playlist = Playlist(uri='cdda://', name="%s - %s"%(artistname,album.name), tracks=sorted(tracks,lambda x,y: cmp(x.track_no,y.track_no)))
        self._playlists['cdda://']=playlist
        listener.BackendListener.send('playlists_loaded')

    def save(self, playlist):
        pass
