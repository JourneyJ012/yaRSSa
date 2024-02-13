import socket
import webbrowser
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'back')))
from file_management import add_url #IMPORT SOMETHING LATER


HOST = "127.0.0.1"
PORT = 8080

def handle_request(client_socket) -> None:
    request_data = client_socket.recv(1024).decode()
    #print("Received request data:", repr(request_data))
    try: #if request_lines but less error prone
        request_lines = request_data.split("\r\n")
        method, path, _ = request_lines[0].split()
    except:
        client_socket.sendall(b'HTTP/1.1 400 Bad Request\r\n\r\n')
    
    
    if method == "GET":
        if path == "/style.css":
            try:
                with open("Front/style.css", "r") as f:
                    response_data = f.read()
            except FileNotFoundError:
                response_data = "CSS file not found"
                #print(response_data)
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/css\r\nContent-Length: {len(response_data)}\r\n\r\n{response_data}" #CSS
        else:
            try:
                with open("Front/index.html", "r") as f:
                    response_data = f.read()
            except FileNotFoundError:
                response_data = "index.html file not found"
                #print(response_data)
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(response_data)}\r\n\r\n{response_data}"
    else: #POST
        body_start = request_data.find("\r\n\r\n") + len("\r\n\r\n")
        form_data = request_data[body_start:]
        #print(f"Before: {form_data}")
        form_data = format_data(form_input=form_data)
        add_url(dir="Back/user_feeds.txt",url=form_data)

        response_data = f"<h1>Form received:</h1><p>{form_data}</p>"
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(response_data)}\r\n\r\n{response_data}"
    
    client_socket.sendall(response.encode())
    client_socket.close()

def format_data(form_input: str) -> str:
    form_input = form_input.split("=", 1)  # Splits from the first '=', outputting https%3A%2F%2Ffeeds.megaphone.fm%2Fnewheights
    form_input = form_input[1].strip().replace("%3A", ":").replace("%2F", "/").replace("%2f", "/")
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

    print("Serving on 127.0.0.1:8080")
    print("Attempting to open in new tab! If there are any problems report them!")
    webbrowser.open_new_tab("http://127.0.0.1:8080")
    main()