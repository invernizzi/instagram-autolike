import requests
import time
import random


CLIENT_ID = 'XXX'  # Create an Instagram app to get this
ACCESS_TOKEN = "XXX"  # ...and this
MY_USER_NAME = 'XXX'  # Your name on instagram
USER_NAME_TO_GIVE_LOTS_OF_LIKES = '<3<3' # The name of the person you want to
                                         # like
MAX_PHOTOS_TO_LIKE_PER_EXECUTION = 3


def wait(min_time, max_time):
    wait_time = random.randint(min_time, max_time)
    print 'Waiting for %d seconds..' % wait_time
    time.sleep(wait_time)
    print 'Back to work'


def iphone_web(url, action='GET', params={}):
    default_params = {'access_token': ACCESS_TOKEN, 'client_id': CLIENT_ID}
    call = {'GET': requests.get, 'POST': requests.post}
    # Rate limit the requests
    wait(1, 5)
    return call[action](
        url,
        params=dict(default_params.items() + params.items()),
        headers={
            'User-Agent': 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7',
            "Content-type": "application/x-www-form-urlencoded"
        }
    ).json()


def like_photo(pictureId):
    like_url = "https://api.instagram.com/v1/media/%s/likes" % pictureId
    if [d for d in iphone_web(like_url)['data'] if d['username'] == MY_USER_NAME]:
        # We already liked this photo, skip
        return False
    else:
        # Like the photo
        iphone_web(like_url, action='POST')
        wait(10, 90)
        return True


def like_user_photos(userId):
    user_media = iphone_web(
        "https://api.instagram.com/v1/users/%s/media/recent/" % user_id)
    liked_photos = 0
    for picture in user_media['data']:
        liked_photos += int(like_photo(picture['id']))
        if liked_photos >= MAX_PHOTOS_TO_LIKE_PER_EXECUTION:
            break


def get_user_id_from_name(name):
    return [
        d['id']
        for d in iphone_web(
            'https://api.instagram.com/v1/users/search',
            params={'q': name}
        )['data']
        if d['username'] == 'veganbondwife'][0]


def enable_requests_logging():
    # This is just to see what's going on on the wire.
    import logging
    import httplib
    httplib.HTTPConnection.debuglevel = 1
    # you need to initialize logging, otherwise you will not see anything from
    # requests
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

enable_requests_logging()
user_id = get_user_id_from_name(USER_NAME_TO_GIVE_LOTS_OF_LIKES)
like_user_photos(user_id)
