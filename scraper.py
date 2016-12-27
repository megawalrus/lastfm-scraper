from bs4 import BeautifulSoup
import re

# sections = soup.find_all(True, attrs={"class" : "tracklist-section"})
# tracks = sections[0].find_all(True, attrs={"class" : " js-link-block js-lazy-buylinks-focus-container "})

# tracks[0].find(True, attrs={"class" : "chartlist-ellipsis-wrap"})

def string_or_none(span):
    if span is not None:
        result = span.string
        if result is not None:
            return result

    return None


def get_scrobbles(page_soup):
    '''
    get_scrobbles: takes a soup object from the html of a last fm
    scrobble list page, and returns a list of the raw html sections
    that holds the information necessary to identify tracks
    '''

    scrobble_sieve = " js-link-block js-lazy-buylinks-focus-container "
    return page_soup.find_all(True, attrs={"class" : scrobble_sieve})


def scrobble_t_info(scrobble):
    t_info_sieve = "chartlist-ellipsis-wrap"
    result = scrobble.find(True, attrs={"class" : t_info_sieve})
    if result is not None:
        return result
    else:
        return None


def t_info_artist(t_info):
    '''
    t_info_artist: takes a t_info (retrieved from a scrobble)
    and returns the artist name from the t_info upon success

    returns None upon failure
    '''
    artist_sieve = "chartlist-artists"
    span = t_info.find(True, attrs={"class" : artist_sieve})
    if span is not None:
        link = span.a
        return string_or_none(link)

    return None


def t_info_spacer(t_info):
    '''
    t_info_spacer: takes a t_info (retrieved from a scrobble)
    and returns the spacer used to separate the artist name from
    the track name in the combined artist track chunk

    returns None upon failure
    '''
    spacer_class = "artist-name-spacer"
    span = t_info.find(True, attrs={"class" : spacer_class})

    return string_or_none(span)


def t_info_song(t_info):
    '''
    t_info_song: takes a t_info (retrieved from a scrobble)
    and returns the song name from the t_info upon success
    returns None upon failure
    '''

    track_sieve = "link-block-target"
    span = t_info.find(True, attrs={"class" : track_sieve})

    return string_or_none(span)


def scrobble_timestamp(scrobble):
    '''
    scrobble_timestamp: takes a scrobble and returns the timestamp
    of the scrobble

    returns None upon failure
    '''
    timestamp_sieve = "chartlist-delete"
    span = scrobble.find(True, attrs={"class" : timestamp_sieve})
    time_tag = span.find(True, attrs={"name" : "timestamp"})
    pattern = re.compile("[0-9]+")
    find = re.search(pattern, str(time_tag))
    if find is not None:
        return find.group(0)
    else:
        return None


def new_listen(artist, track, time):
    if artist is None or track is None or time is None:
        return None

    listen = {}
    listen["artist"] = artist
    listen["track"] = track
    listen["time"] = time

    return listen


def get_listens(page_soup):
    '''
    get_listens: takes a soup object from the html of a last fm scrobbles
    list page, and returns a list of 'listens'
    '''

    scrobbles = get_scrobbles(page_soup)

    


