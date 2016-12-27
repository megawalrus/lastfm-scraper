from bs4 import BeautifulSoup
import requests


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
    time_string = None
    timestamp_sieve = "chartlist-timestamp"
    td = scrobble.find(True, attrs={"class" : timestamp_sieve})
    if td is not None:
        span = td.span
        if span is not None:
            time_string = span.get("title")

    return time_string


def new_listen(artist, track, time):
    if artist is None or track is None or time is None:
        return None

    listen = {}
    listen["artist"] = artist
    listen["track"] = track
    listen["time"] = time

    return listen


def get_next_page(page_soup, prev_url):
    '''
    get_next_page: takes a BeautifulSoup tree representing
    a last.fm page, and returns the link to the next page
    of records of scrobbles
    '''
    href = None
    pagination_filter = "pagination"
    span = page_soup.find(True, attrs={"class" : pagination_filter})
    if span is not None:
        next_filter = "next"
        li = span.find(True, attrs={"class" : next_filter})
        if li is not None:
            a = li.a
            if a is not None:
                href = a.get('href')

    if href is not None:
        if href[0] is '?':
            chunks = prev_url.split('?')
            new = chunks[0] + "?" + href[1:]
            href = new

    return href 


def get_listens(page_soup):
    '''
    get_listens: takes a soup object from the html of a last fm scrobbles
    list page, and returns a list of 'listens'
    '''
    listen_list = []

    scrobbles = get_scrobbles(page_soup)
    for scrobble in scrobbles:
        t_info = scrobble_t_info(scrobble)
        artist = t_info_artist(t_info)
        song = t_info_song(t_info)
        time = scrobble_timestamp(scrobble)
        listen = new_listen(artist, song, time)
        listen_list.append(listen)

    return listen_list


def scrape_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    listens = get_listens(soup)
    next_page = get_next_page(soup, url)

    return (listens, next_page)


def get_five(url):
    listens = []
    count = 0
    curr_url = url
    while(count < 5):
        count += 1
        new_listens, next_page = scrape_page(curr_url)
        listens += new_listens
        curr_url = next_page

    return (len(listens),  listens)

def get_all(url):
    listens = []
    # count = 0
    curr_url = url
    while(curr_url is not None):
        # count += 1
        new_listens, next_page = scrape_page(curr_url)
        listens += new_listens
        curr_url = next_page

    return (len(listens),  listens)
