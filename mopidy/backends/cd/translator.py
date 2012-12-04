from __future__ import unicode_literals

import logging

from mopidy.models import Track, Artist, Album

import audiotools


logger = logging.getLogger('mopidy.backends.cd')

def read_cd(device_path):
    r"""
    Read the cd contents using audiotools.CDDA.

    It expects the cd device name as argument and returns a tuple of ([Track],Album,[Artist])
    """
    try:
        cd=audiotools.CDDA(device_path)
    except Exception, e:
        logger.warn('Something went wrong when reading device %s:\n%s',device_path,e)
        return ([],None,[])
    if len(cd)==0:
        logger.info('No music cd found with valid tracks.')
        return ([],None,[])
    metadata=cd.metadata_lookup()
    music_brainz=False
    if len(metadata[1])>len(metadata[0]) or metadata[0][0].track_name==None or metadata[0][0].album_name==None or metadata[0][0].artist_name==None:
        #only use freedb metadata if musicbrainz metadata seems to be unavailable
        metadata=metadata[1]
    else:
        #else use musicbrainz (preferred)
        metadata=metadata[0]
    artists=dict([(n,Artist(uri="cdda://",name=n)) for n in set([t.artist_name for t in metadata])])
    album=Album(
        uri='cdda://',
        name=metadata[0].album_name,
        artists=artists.values(),
        num_tracks=len(metadata),
        date=metadata[0].date or metadata[0].year)
    tracks=[]
    for i,t in enumerate(metadata):
        tracks.append(
            Track(
                uri='cdda://%i'%t.track_number,
                name=t.track_name,
                artists=[artists[t.artist_name]],
                album=album,
                track_no=t.track_number,
                date=t.date or t.year,
                length=int(round(cd[i+1].length()/75.0*1000,0)),
                bitrate=1411
            ))
    return (tracks,album,artists.values())
