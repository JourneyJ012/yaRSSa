import socket

HOST = "127.0.0.1"
PORT = 8080

def handle_request(client_socket):
    request_data = client_socket.recv(1024).decode()
    response_body = "hello_world"
    response = f"HTTP/1.1 200 OK \r\nContent-length: {len(response_body)}\r\n\r\n{response_body}"
    client_socket.sendall(response.encode())
    client_socket.close()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)

        while True:
            client_socket, addr = server_socket.accept()
            handle_request(client_socket)
    

if __name__ == "__main__":
    main()