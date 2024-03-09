# Yet another RSS app

A simple RSS app in python that doesn't have sponsored content, ads or other crap.


## Features

- Add RSS feeds (not rn currently, major importance)
- Get specific items from RSS feeds (image, url, etc)
- allow removal of feeds from the site


## Todo (closely ordered to when it comes out)

- fix get RSS feeds not working
- restructure the code for `front/socket_stuff.py`'s `format_data` function.
- mark items as read
- fix the end of the last feed and the start of the first feed from showing up on the same line
- fix Apostrophe's appearing as `â€™s`
- make specific errors for every problem (est: march)
- flaresolverr support (further future)
- plugins (further future)


## Known Problems

- error.txt has no leading 0's for date
- Apostrophe's appear as `â€™s`
- the end of the last feed and the start of the first feed from showing up on the same line
- Doesn't work on Brave browser
- Non-existant elements on ANY item will cause a full crash (to be focused on first)
- Python may keep the port used after throwing an error.
- Any URL with `"&RSS_url="` will not work due to how the code is made. If you wish to try fix this, look into `front/socket_stuff.py`'s `format_data` function. 

## Installation

1. Have python installed 

### Untested, but most likely python 3.6+, due to use of dictionaries.

https://python.org

2. Clone the repo

`git clone https://github.com/JourneyJ012/yaRSSa`

3. Navigate in

`cd yaRSSa`


## Usage

### start.bat

`./start.bat`

### start.sh

```
chmod +x start.sh
./start.sh
```


## Errors

The reporting system is yet to be added. Both `start.bat` and `start.sh` only writes the exception to `error.txt` so far. 