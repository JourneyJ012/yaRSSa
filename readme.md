# Yet another RSS app

A simple RSS app in python that doesn't have sponsored content, ads or other crap.


## Features

- Add RSS feeds
- Get specific items from RSS feeds (image, url, etc)


## Todo (closely ordered to when it comes out)

- fix IndexError (est: feb)
- make specific errors for every problem (est: march)
- flaresolverr support (further future)
- plugins (further future)


## Known Problems

- Doesn't work on Brave browser
- Non-existant elements on ANY item will cause a full crash (to be focused on first)
- Python may keep the port used after throwing an error.


## Installation

1. Have python installed 

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