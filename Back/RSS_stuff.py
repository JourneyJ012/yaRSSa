import requests
import xml.etree.ElementTree as ET
import os

def parse_url(url: str, dir: str):
    user_choices: list = get_choices(dir=dir)
    
    feed = requests.get(url=url)
    root = ET.fromstring(str(feed.content.decode()))
    
    with open("Back/test.xml", "w") as f:
        f.write(str(feed.content.decode()))
    
    items = root.findall(".//item")
    results = []
    
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

if __name__ == "__main__":

    parse_url(
        url="http://127.0.0.1:9117/api/v2.0/indexers/1337x/results/torznab/api?apikey=979bnwxk5av7s2lubes71ujymc60m90u&t=search&cat=&q=EPUB",
        dir="back/user_choices.txt")