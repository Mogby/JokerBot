import os
import pickle
import urllib.request

from time import sleep


class PostsDownloader:
  def __init__(self, api, download_content, download_photos, data_directory,
               batch_size, vk_api_requests_interval, http_requests_interval):
    self._api = api

    self._download_content = download_content
    self._download_photos = download_photos

    self._data_directory = data_directory

    self._batch_size = batch_size
    self._vk_api_requests_interval = vk_api_requests_interval
    self._http_requests_interval = http_requests_interval

  def download(self, wall_owner, owner_is_group):
    self._owner_id = self._get_owner_id(wall_owner, owner_is_group)
    self._data_prefix = os.path.join(self._data_directory, wall_owner)

    print('Initializing directories')
    self._init_dirs()
    if self._download_content:
      print('Downloading posts contents')
      self._download_posts_contents()
      print('Saving posts contents')
      self._save_posts()
    if self._download_photos:
      print('Saving attached photos')
      self._save_attached_photos()

  def _init_dirs(self):
    if not os.path.isdir(self._data_prefix):
      os.makedirs(self._data_prefix)
    photos_prefix = self._get_path('photos')
    if not os.path.isdir(photos_prefix):
      os.makedirs(photos_prefix)

  def _download_posts_contents(self):
    batch_size = self._batch_size

    self._posts = []
    offset = 0
    while True:
      posts_batch = self._api.wall.get(owner_id=self._owner_id,
                                       count=batch_size, offset=offset)
      self._posts += posts_batch['items']

      progress_percent = 100 * len(self._posts) // posts_batch['count']
      print('Downloaded ', len(self._posts),
            ' posts out of ', posts_batch['count'],
            ' (', progress_percent, '%)', sep='')

      if len(self._posts) == posts_batch['count']:
        return

      offset += batch_size
      sleep(self._vk_api_requests_interval)

  def _save_attached_photos(self):
    for i, post in enumerate(self._posts):
      percentage = (i + 1) * 100 // len(self._posts)
      print('Saving photos for post ',
            i + 1, ' out of ', len(self._posts),
            ' (', percentage, '%)', sep='')

      if 'attachments' not in post:
        continue

      for attachment in post['attachments']:
        if attachment['type'] == 'photo':
          if self._save_photo(attachment['photo']):
            print('SAVE SUCCESS')
          else:
            print('SAVE FAILURE')

  def _save_photo(self, photo):
    size_priorities = ['x', 'y', 'q', 'r', 'z', 'w', 's', 'm', 'o', 'p']
    for size in size_priorities:
      if self._save_photo_of_size(photo, size):
        return True
    return False

  def _save_photo_of_size(self, photo, desired_size):
    for size in photo['sizes']:
      if size['type'] == desired_size:
        url = size['url']
        path = os.path.join(
          self._get_path('photos'),
          url.split('/')[-1]
        )
        if os.path.isfile(path):
          return True

        try:
          urllib.request.urlretrieve(url, path)
          sleep(self._http_requests_interval)
        except:
          return False

        return True
    return False

  def _save_posts(self):
    with open(self._get_path('posts.pickle'), 'wb') as f:
      pickle.dump(self._posts, f, pickle.HIGHEST_PROTOCOL)

  def _get_path(self, rel_path):
    return os.path.join(
      self._data_prefix,
      rel_path
    )

  def _get_owner_id(self, wall_owner, owner_is_group):
    api = self._api

    try:
      wall_owner = int(wall_owner)
    except:
      # wall owner is not an id, so we need to convert it
      if owner_is_group:
        wall_owner = api.groups.getById(group_id=wall_owner)[0]['id']
      else:
        wall_owner = api.users.get(user_ids=wall_owner)[0]['id']

    if owner_is_group and wall_owner > 0:
      # groups have negative ids
      wall_owner = -wall_owner
    elif not owner_is_group:
      # people have positive ids so if wall_owner is a negative number
      # at this point, this is probably a mistake
      assert(wall_owner > 0)

    return wall_owner
