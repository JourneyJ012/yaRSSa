def add_url(dir: str, url: str) -> str:
    with open(dir, 'r') as file:
        lines = [line.strip() for line in file.readlines()]

    try:

        if url not in lines:
            # If not, append it
            lines.append(url)

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
        return f"Unbound Local Error in function add_url({dir},{url})\n(Back/file_management.py)"