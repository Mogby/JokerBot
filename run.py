#!/usr/bin/env python3

import argparse
import configparser
import json
import vk

from joker.download import PostsDownloader


def load_config():
  with open('config.json', 'r') as f:
    return json.load(f)


def get_api(config):
  print('Trying authorization with token')
  try:
    session = vk.Session(access_token=config['access_token'])
    return vk.API(session, v=config['api_version'])
  except:
    print('Failed')

  print('Trying authorization with user credentials')
  try:
    session = vk.AuthSession(app_id=config['app_id'],
                             user_login=config['login'],
                             user_password=config['password'])
    return vk.API(session, v=config['api_version'])
  except:
    print('Failed')

  return None


def main():
  parser = argparse.ArgumentParser(description='Download posts from a wall in VK.')
  parser.add_argument('--config', '-c', type=str,
                      default='joker.cfg',
                      help='path to config file', metavar='<file>')
  args = parser.parse_args()

  config = configparser.ConfigParser()
  config.read(args.config)

  api = get_api(config['vk_api'])
  if api is None:
    return

  downloader = PostsDownloader(
    api,
    bool(config['downloader']['download_content']),
    bool(config['downloader']['download_photos']),
    config['downloader']['data_directory'],
    int(config['downloader']['batch_size']),
    float(config['downloader']['vk_api_requests_interval']),
    float(config['downloader']['http_requests_interval'])
  )
  downloader.download(
    config['downloader'].get('wall_owner'),
    config['downloader'].getboolean('owner_is_group')
  )


if __name__ == '__main__':
  main()
