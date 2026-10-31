import json
import socket

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("127.0.0.1", 8080))
server.listen(5)
print("Server is running")

while True:
    client, add = server.accept()
    raw = client.recv(2048).decode("utf-8", errors="ignore")



    if not raw:
        client.close()
        continue

    parts = raw.split("\r\n\r\n", 1)
    head = parts[0]
    if len(parts) > 1:
     body = parts[1]
    else:
     body = ""

    lines = head.splitlines()
    first = lines[0].split()
    method = first[0]
    url = first[1]

    params = {}

    if "?" in url:
        path, q = url.split("?", 1)
        if "=" in q:
            k, v = q.split("=", 1)
            params[k] = v

    else:
        path = url

    headers = {}

    for line in lines[1:]:
        if ":" in line:
            k, v = line.split(":", 1)
            headers[k.strip()] = v.strip() 

# GET section~~~\

    if method == "GET":
        param_id = params.get("id", "none")
        resp = f"Yo, ours query id is: {param_id}"
        status = "200 OK"
        content_type = "text/plain"

    else:
        resp = "Method Not Allowed"
        status = "405 Method Not Allowed"
        content_type = "text/plain"

    response = (
        f"HTTP/1.1 {status}\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(resp.encode('utf-8'))}\r\n"
        "Connection: close\r\n\r\n"
        f"{resp}"
    )

    client.sendall(response.encode("utf-8"))
    client.close()