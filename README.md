# JokerBot

(Actually it is not a bot).

My script for handling data from vk.

Currently it can only download posts from a single wall in vk and save their text and attached photos.

## Requirements

This script requires Python 3 to run. Also make sure to install the libraries listed in `requirements.txt` (you can use `pip install -r requirements.txt`).

## Run

To run the script you need to create a config file.
Use `joker_template.cfg` as a template.

Set your `app_id` (read how to create an app for vk to learn how to get this) and your `access_token` (or use your `login` and `password` instead of token).

Replace `wall_owner` with the id of the owner of the wall you wish to scrape.
The following formats are accepted for `wall_owner`:
 - for __groups__ (for example https://vk.com/apiclub) you can use _id number_ (`1`), negative _id number_ (`-1`) or short name (`apiclub`),
 - for __users__ (for example https://vk.com/durov) you can use _id number_ (`1`), `id` + _id number_ (`id1`) or short name (`durov`). 

If you want to download posts from a group `owner_is_group` to `true`. For example, if you set `wall_owner` to `1` and `owner_is_group` to `true`, the posts will be downloaded from https://vk.com/apiclub instead of https://vk.com/durov .

Finally set `data_directory` to the path where you want to store downloaded data.

Now that you have your config ready, run the `run.py` script and pass the path to the config file to it as a command line argument (if you don't provide the path to the config to the script, it will try to use `joker.cfg` in current working directory).

### Usage

```
usage: run.py [-h] [--config <file>]

Download posts from a wall in VK.

optional arguments:
  -h, --help            show this help message and exit
  --config <file>, -c <file>
                        path to config file
```