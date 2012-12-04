from __future__ import unicode_literals

import logging

from mopidy import settings
from mopidy.backends import base
from mopidy.models import Album

from .translator import read_cd

logger = logging.getLogger('mopidy.backends.cd')


class CdLibraryProvider(base.BaseLibraryProvider):
    def __init__(self, *args, **kwargs):
        super(CdLibraryProvider, self).__init__(*args, **kwargs)
        self._uri_mapping=dict()
        self._album=None
        self._artists=[]
        self._tracks=[]
        self.refresh()

    def refresh(self, uri=None):
        logger.info(
            'Loading tracks from %s',
            settings.CD_DEVICE_PATH)

        self._tracks,self._album,self._artists = read_cd(settings.CD_DEVICE_PATH)
        if len(self._tracks)==0:
            logger.info('No tracks found')
            return
        tracks=self._tracks

        for track in tracks:
            self._uri_mapping[track.uri] = track

    def lookup(self, uri):
        try:
            return [self._uri_mapping[uri]]
        except KeyError:
            logger.debug('Failed to lookup %r', uri)
            return []

    def find_exact(self, **query):
        self._validate_query(query)
        result_tracks = self._uri_mapping.values()

        for (field, values) in query.iteritems():
            if not hasattr(values, '__iter__'):
                values = [values]
            # FIXME this is bound to be slow for large libraries
            for value in values:
                q = value.strip()

                track_filter = lambda t: q == t.name
                album_filter = lambda t: q == getattr(t, 'album', Album()).name
                artist_filter = lambda t: filter(
                    lambda a: q == a.name, t.artists)
                uri_filter = lambda t: q == t.uri
                any_filter = lambda t: (
                    track_filter(t) or album_filter(t) or
                    artist_filter(t) or uri_filter(t))

                if field == 'track':
                    result_tracks = filter(track_filter, result_tracks)
                elif field == 'album':
                    result_tracks = filter(album_filter, result_tracks)
                elif field == 'artist':
                    result_tracks = filter(artist_filter, result_tracks)
                elif field == 'uri':
                    result_tracks = filter(uri_filter, result_tracks)
                elif field == 'any':
                    result_tracks = filter(any_filter, result_tracks)
                else:
                    raise LookupError('Invalid lookup field: %s' % field)
        return result_tracks

    def search(self, **query):
        self._validate_query(query)
        result_tracks = self._uri_mapping.values()

        for (field, values) in query.iteritems():
            if not hasattr(values, '__iter__'):
                values = [values]
            # FIXME this is bound to be slow for large libraries
            for value in values:
                q = value.strip().lower()

                track_filter = lambda t: q in t.name.lower()
                album_filter = lambda t: q in getattr(
                    t, 'album', Album()).name.lower()
                artist_filter = lambda t: filter(
                    lambda a: q in a.name.lower(), t.artists)
                uri_filter = lambda t: q in t.uri.lower()
                any_filter = lambda t: track_filter(t) or album_filter(t) or \
                    artist_filter(t) or uri_filter(t)

                if field == 'track':
                    result_tracks = filter(track_filter, result_tracks)
                elif field == 'album':
                    result_tracks = filter(album_filter, result_tracks)
                elif field == 'artist':
                    result_tracks = filter(artist_filter, result_tracks)
                elif field == 'uri':
                    result_tracks = filter(uri_filter, result_tracks)
                elif field == 'any':
                    result_tracks = filter(any_filter, result_tracks)
                else:
                    raise LookupError('Invalid lookup field: %s' % field)
        return result_tracks

    def _validate_query(self, query):
        for (_, values) in query.iteritems():
            if not values:
                raise LookupError('Missing query')
            for value in values:
                if not value:
                    raise LookupError('Missing query')
