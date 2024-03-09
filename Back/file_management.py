from time import localtime
import csv
def handle_error(error) -> None:
    time = localtime()
    time.tm_hour
    try:
        with open("error.txt","a") as f:
            f.write(f"{time.tm_mday}/{time.tm_mon} {time.tm_hour}:{time.tm_min}:{time.tm_sec}: {error}\n")
    except:
        print(f"Error {error}, and error.txt not found!")
        raise FileNotFoundError
    
    
def add_url(dir: str, url: str) -> str:
    with open(dir, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
        print(lines)
        name, url, = url
    try:

        if url not in lines:
            # If not, append it
            lines.append(f"{name},{url}")

            # Write the updated content back to the file
            with open(dir, 'w') as file:
                for line in lines:
                    file.write(line + '\n')
            print(f"URL {url} appended to {dir}")
            return f"Successfully added RSS feed"
        
        else:
            print(f"URL {url} already present in {dir}")
            return f"Already present RSS feed"
        
    except UnboundLocalError:
        
        handle_error(f"Unbound Local Error in function add_url({dir},{url})\n(Back/file_management.py)")
        return f"Unbound Local Error in function add_url({dir},{url})\n(Back/file_management.py)"
    
def remove_feed(name, feeds_dir):
    try:
        with open(feeds_dir, "r") as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        index_to_remove = None
        for i, row in enumerate(rows):
            if row and row[0] == name:
                index_to_remove = i
                break  # Once found, exit loop
        
        if index_to_remove is not None:
            del rows[index_to_remove]
        
        # Filter out empty rows
        rows = [row for row in rows if row]
        
        with open("Back/user_feeds.csv", 'w', newline='') as f:  # Add newline='' to prevent extra line breaks
            writer = csv.writer(f)
            writer.writerows(rows)

    except FileNotFoundError:
        handle_error("FileNotFoundError in Back/remove_url")
        print(f"FileNotFoundError, check error.txt for more details!")
    print(name)