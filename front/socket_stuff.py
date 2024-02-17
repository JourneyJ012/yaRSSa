import socket
import webbrowser
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'back')))
from file_management import add_url #IMPORT SOMETHING LATER
from RSS_stuff import parse_url

HOST = "127.0.0.1"
PORT = 8080

def handle_request(client_socket) -> None:
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
        else:
            try:
                with open("Front/index.html", "r") as f:
                    response_data = f.read()
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(response_data)}\r\n\r\n{response_data}"
            except FileNotFoundError:
                response_data = "index.html file not found"
                response = f"HTTP/1.1 404 Not Found"
    elif method == "POST":
        body_start = request_data.find("\r\n\r\n") + len("\r\n\r\n")
        form_data = request_data[body_start:]

        # Check which button was clicked
        if "new_RSS" in request_data:
            form_data = format_data(form_input=form_data)
            added = add_url(dir="Back/user_feeds.txt", url=form_data)

            if added == "Already present RSS feed" or added == "Successfully added RSS feed":
                response_data = f"<h1>Form received:</h1><p>Feed {form_data} added!</p>"
            else:
                response_data = f"<h1>Fail!</h1><p>{added}</p>"
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(response_data)}\r\n\r\n{response_data}"

        elif "get_RSS" in request_data: 
            
            feeds = parse_url(
                user_feeds_dir="Back/user_feeds.txt",
                user_choices_dir="Back/user_choices.txt"
                )
            with open("Front/style.css","r") as f:
                style = f.read()
                response_data = f"<head><style>{style}</style></head><body><h1>Feeds</h1><p>{feeds}</p></body>"
                print(style)

            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(response_data)}\r\n\r\n{response_data}"
        else:
            response = f"HTTP/1.1 500 Internal Server Error"
            
    
    client_socket.sendall(response.encode())
    #print(response.encode())
    client_socket.close()

def format_data(form_input: str) -> str:
    form_input = form_input.split("=", 1)  # Splits from the first '=', outputting https%3A%2F%2Ffeeds.megaphone.fm%2Fnewheights
    form_input = form_input[1].strip().replace("%3A", ":").replace("%2F", "/").replace("%2f", "/") #Todo: fix this behaviour
    #print(f"After: {form_input}")
    return form_input

def main() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Server listening on {HOST}:{PORT}")

        while True:
            client_socket, addr = server_socket.accept() #SAYS ADDR IS NOT ACCESSED, DOESN'T WORK WITHOUT
            handle_request(client_socket)
    

if __name__ == "__main__":

    print("Attempting to open in new tab! If there are any problems report them!")
    main()
    webbrowser.open_new_tab("http://127.0.0.1:8080") 