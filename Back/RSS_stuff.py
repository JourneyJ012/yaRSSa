import xml.etree.ElementTree as ET
import aiohttp
import asyncio

import aiohttp.client_exceptions
from file_management import handle_error


async def fetch_feed(session, feed_name, url):
    try:
        async with session.get(url) as response:
            response.raise_for_status()  # Raise an error for non-200 status codes
            response_text = await response.text()
            return response_text
        
    except aiohttp.ClientResponseError as e:
        print(f"{feed_name} ({url}) gave error code {e.status}")
    except aiohttp.client_exceptions.InvalidURL:
        print(f"Invalid URL {url}")
        handle_error(f"Invalid URL {url}")
    except aiohttp.client_exceptions.ClientConnectorError:
        print(f"URL {url} could not connect. This error has not been logged.")
    except aiohttp.client_exceptions.ClientOSError as e:
        if "[WinError 64] The specified network name is no longer available]" in str(e):
            print(f"{url} cannot be found. The website could be gone, or it may be a DNS issue.")
    except ConnectionResetError as e:
        if "[WinError 10054 An existing connection was forcibly closed by the remote host]":
            print(f"{url} rejected you.")
    except aiohttp.client_exceptions.ServerDisconnectedError:
        print(f"Server disconnected ({url})")



async def fetch_all_feeds(session, user_feeds):
    tasks = []
    for feed_name, url in user_feeds.items():
        tasks.append(fetch_feed(session, feed_name, url))
    return await asyncio.gather(*tasks)

async def parse_feed_content(session, user_feeds_dir: str, user_choices_dir: str):

    user_choices = get_choices(user_choices_dir)
    user_feeds = get_feeds(user_feeds_dir)
    # returns a list of feeds.
    user_feeds = await fetch_all_feeds(session, user_feeds=user_feeds)
    results = []
    for feed_content in user_feeds:
        try:
            root = ET.fromstring(feed_content)
            feed_items = []
            items = root.findall(".//item")
            # print(items)
            for item in items:
                current_item = []
                for choice in user_choices:
                    found_element = item.find(choice)
                    if found_element is not None:
                        choice_text = found_element.text
                        current_item.append(choice_text)
                    else:
                        #print(f"Could not find {choice} in {item}")
                        pass

                feed_items.append(current_item)
            results.append(feed_items)
        except Exception as e:
            results.append(str(f"Error: {e}"))

    final_results = []
    has_title, has_link = False, False
    if "title" in user_choices:
        title_index = user_choices.index("title")
        has_title = True
    if "link" in user_choices:
        link_index = user_choices.index("link")
        has_link = True
    for sublist in results:
        inner_result = []
        for item in sublist:
            if has_link and has_title:
                try:
                    temp_result = f"<a href='{item[link_index]}'>{item[title_index]}</a>"
                except IndexError:
                    temp_result = "URL broken!"
                    handle_error("""Broken URL caused broken response "URL broken!" This is due to an IndexError in Back/RSS_stuff.py. Please check your feeds in user_feeds.csv for any broken feeds.""")
                    break
            else:
                temp_result = ""
            for choice in user_choices:
                if ((choice not in ["title", "link"]) or (has_link == True and has_title == False and choice == "link") or (has_link == False and has_title == True and choice == "title")):
                    try:
                        temp_result += f"<br>{item[user_choices.index(choice)]}"
                    except:
                        pass
            inner_result.append(temp_result)
            inner_result.append("<br>")  # <br> <THIS br> <br>
        # <THIS BR> <br> <THIS BR>
        final_results.append("<br>".join(inner_result))
        # Between feeds, only 1 <br> tag appears. This sucks because 2 are meant to appear.

    results = "\n".join(final_results)
    return results


def get_choices(dir: str):
    with open(dir, "r") as f:
        user_choices = f.readlines()
        user_choices = [choice.strip() for choice in user_choices]
    return user_choices


def get_feeds(dir: str) -> dict:
    with open(dir, "r") as f:
        list_user_feeds: list = f.readlines()
        list_user_feeds = [feed.strip() for feed in list_user_feeds]
        # List ["BBC UK,http://feeds.bbci.co.uk/news/uk/rss.xml",
        # "Sky News UK,http://feeds.skynews.com/feeds/rss/uk.xml]"

        user_feeds: dict = {}

        try:
            for feed_info in list_user_feeds:
                name, url = feed_info.split(",")
                user_feeds[name.strip()] = url.strip()
                # Dict {"BBC UK":"http://feeds.bbci.co.uk/news/uk/rss.xml",
                # "Sky News UK":"http://feeds.skynews.com/feeds/rss/uk.xml"}
        except ValueError:
            handle_error(
                "There's a problem in your Back/user_feeds.csv, where you have either forgotten the title, URL, or comma. Please check your error.")
    return user_feeds
