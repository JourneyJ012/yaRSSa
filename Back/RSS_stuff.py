import requests
import xml.etree.ElementTree as ET
from file_management import handle_error
import asyncio
import aiohttp


async def fetch_feed(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                return await response.text()
        except aiohttp.client_exceptions.InvalidURL:
            print(f"Invalid URL {url}")
            handle_error(f"Invalid URL {url}")

async def parse_url(user_feeds_dir: str, user_choices_dir: str):
    user_choices: list = get_choices(dir=user_choices_dir)
    user_feeds: list = get_feeds(dir=user_feeds_dir)
    results = []

    tasks = [fetch_feed(url) for url in user_feeds]
    responses = await asyncio.gather(*tasks)

    for feed_content in responses:
        try:
            root = ET.fromstring(feed_content)
            feed_items = []
            items = root.findall(".//item")
            for item in items:
                current_item = []
                for choice in user_choices:
                    found_element = item.find(choice)
                    if found_element is None:
                        print(f"Could not find {choice} in {item}")
                    else:
                        choice_text = found_element.text
                        current_item.append(choice_text)
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
                    handle_error("""Broken URL caused broken response "URL broken!" This is due to an IndexError in Back/RSS_stuff.py. Please check your feeds in user_feeds.txt for any broken feeds.""")
            else:
                temp_result = ""
            for choice in user_choices:
                if ((choice not in ["title", "link"]) or (has_link == True and has_title == False and choice == "link") or (has_link == False and has_title == True and  choice == "title")):
                    try:
                        temp_result += f"<br>{item[user_choices.index(choice)]}"
                    except:
                        pass
            inner_result.append(temp_result)
        final_results.append("<br>".join(inner_result))

    results = "\n".join(final_results)

    with open("Back/results.txt","w") as f:
        f.write(str(results))
    return results

def get_choices(dir: str):
    with open(dir,"r") as f:
        user_choices = f.readlines()
        user_choices = [choice.strip() for choice in user_choices]
    return user_choices 

def get_feeds(dir: str):
    with open(dir,"r") as f:
        user_feeds = f.readlines()
        user_feeds = [feed.strip() for feed in user_feeds]
    return user_feeds 

if __name__ == "__main__":
    parse_url(
        user_feeds_dir="Back/user_feeds.txt",
        user_choices_dir="Back/user_choices.txt")