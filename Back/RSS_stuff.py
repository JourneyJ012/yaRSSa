import xml.etree.ElementTree as ET
import aiohttp
import asyncio
from file_management import handle_error

async def fetch_feed(session, feed_name, url):
    try:
        async with session.get(url) as response:
            return await response.text()
    except aiohttp.client_exceptions.InvalidURL:
        print(f"Invalid URL {url}")
        handle_error(f"Invalid URL {url}")
    except aiohttp.client_exceptions.ClientConnectorError:
        print(f"URL {url} could not connect. This error has not been logged.")

async def parse_url(user_feeds_dir: str, user_choices_dir: str): 
#TODO: split the getting of URLs into:
    #Get URLs from a CSV file, as to allow titles of the feeds
    #Make results a dictionary with the title and then the feed
    


    user_choices = get_choices(user_choices_dir)
    user_feeds = get_feeds(user_feeds_dir)
    print(user_feeds)
    results = []

    async with aiohttp.ClientSession() as session:
        for feed_name, url in user_feeds.items():
            feed_content = await fetch_feed(session, feed_name, url)
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
                    handle_error("""Broken URL caused broken response "URL broken!" This is due to an IndexError in Back/RSS_stuff.py. Please check your feeds in user_feeds.csv for any broken feeds.""")
            else:
                temp_result = ""
            for choice in user_choices:
                if ((choice not in ["title", "link"]) or (has_link == True and has_title == False and choice == "link") or (has_link == False and has_title == True and  choice == "title")):
                    try:
                        temp_result += f"<br>{item[user_choices.index(choice)]}"
                    except:
                        pass
            inner_result.append(temp_result)
            inner_result.append("<br>")
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

def get_feeds(dir: str) -> dict:
    with open(dir,"r") as f:
        list_user_feeds: list = f.readlines()
        list_user_feeds = [feed.strip() for feed in list_user_feeds] 
        #List ["BBC UK,http://feeds.bbci.co.uk/news/uk/rss.xml", 
        #"Sky News UK,http://feeds.skynews.com/feeds/rss/uk.xml]"
        
        user_feeds: dict = {}
        
        for feed_info in list_user_feeds:
            name, url = feed_info.split(",")
            user_feeds[name.strip()] = url.strip()
            #Dict {"BBC UK":"http://feeds.bbci.co.uk/news/uk/rss.xml", 
            #"Sky News UK":"http://feeds.skynews.com/feeds/rss/uk.xml"}


    return user_feeds 

if __name__ == "__main__":
    asyncio.run(parse_url(
        user_feeds_dir="Back/user_feeds.csv",
        user_choices_dir="Back/user_choices.txt"
    ))
