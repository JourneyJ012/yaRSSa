import requests
import xml.etree.ElementTree as ET

def parse_url(user_feeds_dir: str, user_choices_dir: str):
    user_choices: list = get_choices(dir=user_choices_dir)
    user_feeds: list = get_feeds(dir=user_feeds_dir)
    results = []
    for url in user_feeds:
        feed = requests.get(url=url)
        root = ET.fromstring(str(feed.content.decode()))
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

    # set up <a> tags
    if all(choice in user_choices for choice in ["title", "link"]):
        title_index = user_choices.index("title")
        link_index = user_choices.index("link")

        results = "\n".join([
            "<br>".join([
                f"<a href='{item[link_index]}'>{item[title_index]}</a>" +
                "".join([f"<br>{item[user_choices.index(choice)]}" for choice in user_choices if choice not in ["title", "link"]])
                for item in sublist
            ]) for sublist in results
        ])
    else: #Todo: fix IndexError
            results = "<br>".join("<br>".join(str(item) for item in sublist) for sublist in results)

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