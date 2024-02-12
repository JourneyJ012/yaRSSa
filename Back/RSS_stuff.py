import requests
import xml.etree.ElementTree as ET

def parse_url(url: str, dir: list): #todo: make a toggle that allows the user to make whatever they want as a toggle
    user_choices = get_choices(dir=dir)
    results = []
    
    feed = requests.get(url=url)

    root = ET.fromstring(str(feed.content.decode()))
    with open("back/test.xml","w") as f:
        f.write(str(feed.content.decode()))
    items = root.findall(".//item")
    for item in items:
        for choice in user_choices:
            current_item = []
            choice = item.find(choice).text
            current_item.append(choice)
            results.append(current_item)



    return results  #Todo: make this into a toggle, then return a dict of what the people want.

def get_choices(dir: str):
    with open(dir,"r") as f:
        user_choices = f.readlines()
    print(user_choices)
    return user_choices

if __name__ == "__main__":
    with open("back/results.txt","w") as f:
        f.write(str(
            parse_url(
                url="http://127.0.0.1:9117/api/v2.0/indexers/1337x/results/torznab/api?apikey=979bnwxk5av7s2lubes71ujymc60m90u&t=search&cat=&q=EPUB")),
                dir="back/user_choices.txt"
                )