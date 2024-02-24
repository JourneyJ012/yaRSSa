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
                temp_result = f"<a href='{item[link_index]}'>{item[title_index]}</a>"
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