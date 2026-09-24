import socket
import threading

TCP_PORT = 8765
DISCOVERY_PORT = 8766
OWNER_CODE = "1234"


def discovery_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(("0.0.0.0", DISCOVERY_PORT))

    print("DISCOVERY READY - Port 8766")

    while True:
        data, address = sock.recvfrom(1024)

        message = data.decode().strip()

        if message == "NOVA_SCAN":

            response = f"NOVA_FOUND|{socket.gethostname()}|{TCP_PORT}"

            sock.sendto(
                response.encode(),
                address
            )

            print("SCAN REQUEST:", address)


def handle_client(client, address):

    print("Connection from:", address)

    try:

        client.sendall(
            b"NOVA_PAIR_REQUIRED\n"
        )

        code = client.recv(1024).decode().strip()

        if code == OWNER_CODE:

            client.sendall(
                b"PAIR_SUCCESS\n"
            )

            print("Device paired successfully.")

        else:

            client.sendall(
                b"PAIR_FAILED\n"
            )

            print("Wrong owner code.")

    except Exception as e:

        print("Connection error:", e)

    finally:

        client.close()


def tcp_server():

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind(
        ("0.0.0.0", TCP_PORT)
    )

    server.listen(10)

    print("NOVA SERVER READY")
    print("TCP Port:", TCP_PORT)
    print("Owner Code:", OWNER_CODE)

    while True:

        client, address = server.accept()

        thread = threading.Thread(
            target=handle_client,
            args=(client, address),
            daemon=True
        )

        thread.start()


threading.Thread(
    target=discovery_server,
    daemon=True
).start()

tcp_server()
