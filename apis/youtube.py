""" Contains functions to fetch info from youtube's API (googleapis.com/youtube/v3/) """
import logging
from utilities import web, string_utili

# YouTube API key.
YOUTUBE_API_KEY = 'AIzaSyCPQe4gGZuyVQ78zdqf9O5iEyfVLPaRwZg'

log = logging.getLogger(__name__)


def youtube_search(search):
    """
    Searches the youtube API for a youtube video matching the search term.

    A json response of ~50 possible items matching the search term will be presented.
    Each video_id will then be checked by youtube_time() until a candidate has been found
    and the resulting dict can be returned.

    :param search: The search term str to search for.
    :return: dict{'type=youtube', 'video_id', 'int(video_time)', 'video_title'} or None on error.
    """
    if search:
        if 'list' in search:
            search = search.split('?list')[0]
        youtube_search_url = 'https://www.googleapis.com/youtube/v3/search?' \
                             'type=video&key=%s&maxResults=50&q=%s&part=snippet' % (YOUTUBE_API_KEY, search)

        response = web.http_get(youtube_search_url, json=True)

        if response['json'] is not None:
            try:
                if 'items' in response['json']:
                    for item in response['json']['items']:
                        video_id = item['id']['videoId']
                        video_title = item['snippet']['title'].encode('ascii', 'ignore')

                        video_time = youtube_time(video_id)
                        if video_time is not None:
                            return {
                                'type': 'youTube',
                                'video_id': video_id,
                                'video_time': video_time['video_time'],
                                'video_title': video_title
                            }
            except KeyError as ke:
                log.error(ke, exc_info=True)
                return None
    else:
        return None


def youtube_search_list(search, results=10):
    """
    Searches the API of youtube for videos matching the search term.

    Instead of returning only one video matching the search term, we return a list of candidates.

    :param search: The search term str to search for.
    :param results: int determines how many results we would like on our list.
    :return: list[dict{'type=youtube', 'video_id', 'int(video_time)', 'video_title'}] or None on error.
    """
    if search:
        youtube_search_url = 'https://www.googleapis.com/youtube/v3/search?type=video' \
                             '&key=%s&maxResults=50&q=%s&part=snippet' % (YOUTUBE_API_KEY, search)

        response = web.http_get(youtube_search_url, json=True)
        if response['json'] is not None:
            media_list = []
            try:
                if 'items' in response['json']:
                    i = 0
                    for item in response['json']['items']:
                        # if i == results:  # if i >= results:
                        #     return media_list
                        # else:
                        #     video_id = item['id']['videoId']
                        #     video_title = item['snippet']['title'].encode('ascii', 'ignore')

                        if i != results:
                            video_id = item['id']['videoId']
                            video_title = item['snippet']['title'].encode('ascii', 'ignore')

                            video_time = youtube_time(video_id)
                            if video_time is not None:
                                media_info = {
                                    'type': 'youTube',
                                    'video_id': video_id,
                                    'video_time': video_time['video_time'],
                                    'video_title': video_title
                                }
                                log.debug('Youtube item %s %s' % (i, media_info))
                                media_list.append(media_info)
                                i += 1
                        else:
                            return media_list
            except KeyError as ke:
                log.error(ke, exc_info=True)
                return None
    else:
        return None


def youtube_playlist_search(search, results=5):
    """
    Searches youtube for a playlist matching the search term.
    :param search: str the search term to search to search for.
    :param results: int the number of playlist matches we want returned.
    :return: list[dict{'playlist_title', 'playlist_id'}] or None on failure.
    """
    if search:
        youtube_search_url = 'https://www.googleapis.com/youtube/v3/search?' \
                             'type=playlist&key=%s&maxResults=50&q=%s&part=snippet' % (YOUTUBE_API_KEY, search)

        response = web.http_get(youtube_search_url, json=True)
        if response['json'] is not None:
            play_lists = []
            try:
                if 'items' in response['json']:
                    for item in response['json']['items']:
                        playlist_id = item['id']['playlistId']
                        playlist_title = item['snippet']['title'].encode('ascii', 'ignore')
                        play_list_info = {
                            'playlist_title': playlist_title,
                            'playlist_id': playlist_id
                        }
                        play_lists.append(play_list_info)
                        if len(play_lists) == results:
                            return play_lists
            except KeyError as ke:
                log.error(ke, exc_info=True)
                return None
    else:
        return None


def youtube_playlist_videos(playlist_id):
    """
    Finds the video info for a given playlist ID.

    The list returned will contain a maximum of 50 videos by default.
    :param playlist_id: str the playlist ID.
    :return: list[dict{'type=youTube', 'video_id', 'video_title', 'video_time'}] or None on failure.
    """
    playlist_details_url = 'https://www.googleapis.com/youtube/v3/playlistItems?' \
                           'key=%s&playlistId=%s&maxResults=50&part=snippet,id' % (YOUTUBE_API_KEY, playlist_id)

    response = web.http_get(playlist_details_url, json=True)
    if response['json'] is not None:
        video_list = []
        try:
            if 'items' in response['json']:
                for item in response['json']['items']:
                    video_id = item['snippet']['resourceId']['videoId']
                    video_title = item['snippet']['title'].encode('ascii', 'ignore')

                    video_time = youtube_time(video_id)
                    if video_time is not None:
                        info = {
                            'type': 'youTube',
                            'video_id': video_id,
                            'video_title': video_title,
                            'video_time': video_time['video_time']
                        }
                        video_list.append(info)
                return video_list
        except KeyError as ke:
            log.error(ke, exc_info=True)
            return None


def youtube_playlist_all_videos(playlist_id):
    """
    Finds the video info for a given playlist ID.

    The list returned will contain all the videos found in the playlist via the page token.
    :param playlist_id: str the playlist ID.
    :return: list[dict{'type=youTube', 'video_id', 'video_title', 'video_time'}] or None on failure &
             the number of videos which were not available to be searched/public.
    """
    _page_token = ''
    playlist_details_url = 'https://www.googleapis.com/youtube/v3/playlistItems?' \
                           'key=%s&playlistId=%s&maxResults=50&part=status,contentDetails&pageToken=%s'

    video_list = []
    _loop_pages = True
    _non_public = 0

    while _loop_pages:
        next_playlist_url = playlist_details_url % (YOUTUBE_API_KEY, playlist_id, _page_token)
        response = web.http_get(next_playlist_url, json=True)
        if response['json'] is not None:
            if 'nextPageToken' in response['json']:
                print('Next Page Token is present.')
                _page_token = str(response['json']['nextPageToken'])
                print(_page_token)
            else:
                print('No Page Token present.')
                _page_token = ''
                _loop_pages = False

            try:
                if 'items' in response['json']:
                    for item in response['json']['items']:
                        if item['status']['privacyStatus'] == 'public':
                            video_id = item['contentDetails']['videoId']

                            # Prevent any checks for a large playlist retrieval of this kind.
                            video_time = youtube_time(video_id, False)
                            if video_time is not None:
                                info = {
                                    'type': 'youTube',
                                    'video_id': video_id,
                                    'video_title': video_time['video_title'],
                                    'video_time': video_time['video_time']
                                }
                                video_list.append(info)
                        else:
                            _non_public += 1
            except KeyError as ke:
                log.error(ke, exc_info=True)
                return None
    return video_list, _non_public


def youtube_time(video_id, check=True):
    """
    Youtube helper function to get the video time for a given video id.

    Checks a youtube video id to see if the video is blocked or allowed in the following countries:
    UK, USA, DENMARK and POLAND. If a video is blocked in one of the countries, None is returned.
    If a video is NOT allowed in ONE of the countries, None is returned else the video time will be returned.

    :param check: bool True = checks region restriction. False = no check will be done
    :param video_id: The youtube video id str to check.
    :return: dict{'type=youTube', 'video_id', 'video_time', 'video_title'} or None
    """
    youtube_details_url = 'https://www.googleapis.com/youtube/v3/videos?' \
                          'id=%s&key=%s&part=contentDetails,snippet' % (video_id, YOUTUBE_API_KEY)

    response = web.http_get(youtube_details_url, json=True)

    if response['json'] is not None:
        try:
            if 'items' in response['json']:
                if len(response['json']['items']) is not 0:
                    contentdetails = response['json']['items'][0]['contentDetails']
                    if check:
                        if 'regionRestriction' in contentdetails:
                            # TODO: Added UK as a country to watch out for, if it restricted.
                            if 'blocked' in contentdetails['regionRestriction']:
                                if ('UK', 'US' or 'DK' or 'PL') in contentdetails['regionRestriction']['blocked']:
                                    log.info('%s is blocked in: %s' %
                                             (video_id, contentdetails['regionRestriction']['blocked']))
                                    return None
                            if 'allowed' in contentdetails['regionRestriction']:
                                if ('UK', 'US' or 'DK' or 'PL') not in contentdetails['regionRestriction']['allowed']:
                                    log.info('%s is allowed in: %s' %
                                             (video_id, contentdetails['regionRestriction']['allowed']))
                                    return None
                    video_time = string_utili.convert_to_millisecond(contentdetails['duration'])
                    video_title = response['json']['items'][0]['snippet']['title'].encode('ascii', 'ignore')

                    return {
                        'type': 'youTube',
                        'video_id': video_id,
                        'video_time': video_time,
                        'video_title': video_title
                    }
                return None
        except KeyError as ke:
            log.error(ke, exc_info=True)
            return None
