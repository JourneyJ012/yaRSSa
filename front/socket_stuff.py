import socket
import sys
import os
import asyncio
import aiohttp
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'back')))
from file_management import handle_error, add_url, remove_feed 
from RSS_stuff import parse_url
#These are imported after the sys.path.append(...) line due to the fact that they are in the ../Back/ folder. 
#If anyone knows of a better solution, please change this.
#However, I would expect errors due to the fact that this has changed the path.

HOST = "127.0.0.1"
PORT = 8080

async def handle_request(client_socket, session) -> None:
    request_data = client_socket.recv(1024).decode()
    #print("Received request data:", repr(request_data))
    try: #if request_lines but less error prone
        request_lines = request_data.split("\r\n")
        method, path, _ = request_lines[0].split()
    except:
        client_socket.sendall(b'HTTP/1.1 500 Internal Server Error')
        return None
    
    try:
        if method in locals() and path in locals():
            print("Variables method and path were found!")
    except UnboundLocalError:
        client_socket.sendall(b'HTTP/1.1 500 Internal Server Error')
        print(f"Variables method and path were not found!")
        return None

    if method == "GET":
        if path == "/style.css":
            try:
                with open("Front/style.css", "r") as f:
                    response_data = f.read()
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/css\r\nContent-Length: {len(response_data)}\r\n\r\n{response_data}" #CSS
            except FileNotFoundError:
                response_data = "CSS file not found"
                response = f"HTTP/1.1 404 Not Found"
                handle_error("File style.css not found")
        else:
            try:
                with open("Front/index.html", "r") as f:
                    response_data = f.read()
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(response_data)}\r\n\r\n{response_data}"
            except FileNotFoundError:
                response_data = "index.html file not found"
                response = f"HTTP/1.1 404 Not Found"
                handle_error("File Front/index.html not found!")
                
    elif method == "POST":
        body_start = request_data.find("\r\n\r\n") + len("\r\n\r\n")
        form_data = request_data[body_start:]

        # Check which button was clicked
        if "RSS_name" in request_data and "RSS_url" in request_data:

            print("new_RSS triggered!")

            form_data = format_data(form_input=form_data, url=True)
            added = add_url(dir="Back/user_feeds.csv", url=form_data)

            if added == "Successfully added RSS feed":
                response_data = f"<h1>Form received:</h1><p>Feed {form_data} added!</p>"
            elif  added == "Already present RSS feed":
                response_data = f"<h1>Form received:</h1><p>Feed {form_data} was already there!"
            else:
                response_data = f"<h1>Fail!</h1><p>{added}</p>"
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(response_data)}\r\n\r\n{response_data}"

        elif "get_RSS" in request_data: #TODO: figure out why it takes each item in the list for finding elements

            print("get_RSS triggered!")

            feeds = await parse_url(
                session=session,
                user_feeds_dir="Back/user_feeds.csv",
                user_choices_dir="Back/user_choices.txt"
            )
            with open("Front/style.css","r") as f:
                style = f.read()
                response_data = f"<head><style>{style}</style></head><body><h1>Feeds</h1><p>{feeds}</p></body>"
                #print(style)

            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(response_data)}\r\n\r\n{response_data}"


        elif "remove_feed" in request_data:
                #remove_feed(feed_url) #TODO: add to file_management
                print("remove_feed triggered!")
                form_data = format_data(form_input=form_data, url=False)
                remove_feed(
                    form_data,
                    "Back/user_feeds.csv")
                
                with open("Front/style.css","r") as f:
                    style = f.read()
                    response_data = f"<head><style>{style}</style></head><body><h1>Feeds</h1><p>{form_data}</p></body>"
                    #print(style)
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(response_data)}\r\n\r\n{response_data}"

        else:
            response = f"HTTP/1.1 500 Internal Server Error"
            handle_error(response)
    
    client_socket.sendall(response.encode())
    #print(response.encode())
    client_socket.close()

def format_data(form_input: str, url: bool) -> str: #sigh. form_input is a list when adding an RSS feed. Don't ask how, but it works. May god have luck on anyone trying to fix that part.

    form_input = form_input.split("=", 1)  # Splits from the first '=', outputting https%3A%2F%2Ffeeds.megaphone.fm%2Fnewheights
    form_input = form_input[1].strip().replace("%3A", ":").replace("%2F", "/").replace("%2f", "/").replace("%2C"," ")

    #TODO: REMAKE THIS WHOLE THING, IT WORKS MAGICALLY BUT SUCKS AND IS A MASSIVE EYESORE.

    if not url: #used for remove_feed
        form_input = form_input.replace("+"," ")
    elif "&RSS_url=" in form_input:
        form_input: list = form_input.split("&RSS_url=")
    print("HERE HERE LOOK HERE", form_input, type(form_input))
    
    if type(form_input == list):
        form_input[0] = form_input[0].replace("+", " ")

    #print(f"After: {form_input}")
    return form_input

async def main() -> None:
    async with aiohttp.ClientSession() as session:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((HOST, PORT))
            server_socket.listen(5)
            print(f"Server listening on {HOST}:{PORT}")

            loop = asyncio.get_event_loop()
            while True:
                client_socket, addr = server_socket.accept() 
                await handle_request(client_socket, session=session)

if __name__ == "__main__":
    print("Attempting to open in new tab! If there are any problems report them!")
    asyncio.run(main())