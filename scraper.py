from bs4 import BeautifulSoup
import re

# sections = soup.find_all(True, attrs={"class" : "tracklist-section"})
# tracks = sections[0].find_all(True, attrs={"class" : " js-link-block js-lazy-buylinks-focus-container "})

# tracks[0].find(True, attrs={"class" : "chartlist-ellipsis-wrap"})


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
    if result:
        return result
    else:
        return None


def t_info_artist(t_info):
    '''
    t_info_artist: takes a t_info (retrieved from a scrobble)
    and returns the artist name from the t_info upon success
    returns None upon failure
    '''


def t_info_song(t_info):
    '''
    t_info_song: takes a t_info (retrieved from a scrobble)
    and returns the song name from the t_info upon success
    returns None upon failure
    '''    


def scrobble_time(scrobble):
    '''
    takes a scrobble and returns the timestamp of the scrobble
    returns None upon failure
    '''


def get_tracks(page_soup):
    '''
    get_tracks: takes a soup object from the html of a last fm scrobbles
    list page, and returns a list of 'tracks'
    '''

    


