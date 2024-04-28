# Yet another RSS app

A simple RSS app in python that doesn't have sponsored content, ads or other crap.


## Features

- Add RSS feeds
- Get specific items from RSS feeds (image, url, etc)
- allow removal of feeds from the site
- duplication check whilst adding


## Todo (closely ordered to when it comes out)

- auto-update functionality
- mark items as read
- fix the end of the last feed and the start of the first feed from showing up with 1 less `<br>`
- fix Apostrophe's appearing as `â€™s`
- make specific errors for every problem
- plugins
- flaresolverr support (further future)


## Known Problems

- error.txt has no leading 0's for date
- Apostrophe's appear as `â€™s`
- the end of the last feed and the start of the first feed from showing up closer
- Python may keep the port used after throwing an error. (can no longer replicate, please provide info if this happens to you)
- Any URL with `"&RSS_url="` will not work. (not planned to be fixed.)

## Installation

1. Have python installed 

### Untested, but most likely python 3.5+, due to async.

https://python.org

2. Clone the repo
`git clone https://github.com/JourneyJ012/yaRSSa`

3. Navigate into the project
`cd yaRSSa`

4. Install requirements
`pip install -r requirements.txt`


## Usage

### start.bat

`./start.bat`

### start.sh

```
chmod +x start.sh
./start.sh
```
