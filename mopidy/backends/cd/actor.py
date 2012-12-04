from __future__ import unicode_literals

import logging

import pykka

from mopidy.backends import base

from .library import CdLibraryProvider
from .playlists import CdPlaylistsProvider

logger = logging.getLogger('mopidy.backends.cd')


class CdBackend(pykka.ThreadingActor, base.Backend):
    def __init__(self, audio):
        logger.info('Loading cd backend')
        super(CdBackend, self).__init__()

        self.library = CdLibraryProvider(backend=self)
        self.playback = base.BasePlaybackProvider(audio=audio, backend=self)
        self.playlists = CdPlaylistsProvider(backend=self)

        self.uri_schemes = ['cdda']
