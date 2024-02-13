import requests
import xml.etree.ElementTree as ET

def parse_url(user_feeds_dir: str, user_choices_dir: str):
    user_choices: list = get_choices(dir=user_choices_dir)
    user_feeds: list = get_feeds(dir=user_feeds_dir)
    print(user_feeds)
    results = []
    for url in user_feeds:
            
        
        
        feed = requests.get(url=url)
        root = ET.fromstring(str(feed.content.decode()))
        
        with open(f"Back/test_.xml", "w") as f: #TODO: MAKE EVERY RSS FEED HAVE AN OUTPUT
            f.write(str(feed.content.decode()))        
        
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
            results.append(current_item)
        
    return results

def get_choices(dir: str):
    with open(dir,"r") as f:
        user_choices = f.readlines()
        for i in range(0,len(user_choices)):
            user_choices[i] = str(user_choices[i]).strip()
    print(user_choices)
    return user_choices 

def get_feeds(dir: str):
    with open(dir,"r") as f:
        user_feeds = f.readlines()
        for i in range(0,len(user_feeds)):
            user_feeds[i] = str(user_feeds[i]).strip()
    print(user_feeds)
    return user_feeds 

if __name__ == "__main__":
    parse_url(
        user_feeds_dir="Back/user_feeds.txt",
        user_choices_dir="Back/user_choices.txt")