import os
import socket
import argparse
from struct import pack

DEFAULT_PORT = 69
BLOCK_SIZE = 512
DEFAULT_TRANSFER_MODE = 'octet'
TIMEOUT = 5

OPCODE = {'RRQ': 1, 'WRQ': 2, 'DATA': 3, 'ACK': 4, 'ERROR': 5}

ERROR_CODE = {
    0: "Not defined, see error message (if any).",
    1: "File not found.",
    2: "Access violation.",
    3: "Disk full or allocation exceeded.",
    4: "Illegal TFTP operation.",
    5: "Unknown transfer ID.",
    6: "File already exists.",
    7: "No such user."
}


def send_rrq(sock, server_address, filename, mode):
    """Send RRQ (Read Request) to the server."""
    format = f'>h{len(filename)}sB{len(mode)}sB'
    rrq_message = pack(format, OPCODE['RRQ'], bytes(filename, 'utf-8'), 0, bytes(mode, 'utf-8'), 0)
    sock.sendto(rrq_message, server_address)


def send_wrq(sock, server_address, filename, mode):
    """Send WRQ (Write Request) to the server."""
    format = f'>h{len(filename)}sB{len(mode)}sB'
    wrq_message = pack(format, OPCODE['WRQ'], bytes(filename, 'utf-8'), 0, bytes(mode, 'utf-8'), 0)
    sock.sendto(wrq_message, server_address)


def receive_file(sock, filename):
    """Handle file download (get)."""
    with open(filename, 'wb') as file:
        expected_block = 1
        while True:
            try:
                data, server = sock.recvfrom(516)
                opcode = int.from_bytes(data[:2], 'big')

                if opcode == OPCODE['DATA']:
                    block_number = int.from_bytes(data[2:4], 'big')
                    if block_number == expected_block:
                        send_ack(sock, block_number, server)
                        file_block = data[4:]
                        file.write(file_block)
                        expected_block += 1

                        if len(file_block) < BLOCK_SIZE:
                            print("File transfer completed.")
                            break
                elif opcode == OPCODE['ERROR']:
                    error_code = int.from_bytes(data[2:4], 'big')
                    print(ERROR_CODE.get(error_code, "Unknown error."))
                    break

            except socket.timeout:
                print("Timeout waiting for DATA.")
                break


def send_file(sock, filename):
    """Handle file upload (put)."""
    try:
        with open(filename, 'rb') as file:
            block_number = 0
            while True:
                block_number += 1
                data_block = file.read(BLOCK_SIZE)
                data_message = pack('>hh', OPCODE['DATA'], block_number) + data_block
                sock.sendto(data_message, server_address)

                try:
                    ack, _ = sock.recvfrom(516)
                    ack_opcode = int.from_bytes(ack[:2], 'big')
                    ack_block = int.from_bytes(ack[2:4], 'big')

                    if ack_opcode == OPCODE['ACK'] and ack_block == block_number:
                        if len(data_block) < BLOCK_SIZE:
                            print("File transfer completed.")
                            break

                except socket.timeout:
                    print("Timeout waiting for ACK.")
                    break

    except FileNotFoundError:
        print("File not found for upload.")


def send_ack(sock, block_number, server):
    """Send ACK for received data block."""
    ack_message = pack('>hh', OPCODE['ACK'], block_number)
    sock.sendto(ack_message, server)


def main():
    parser = argparse.ArgumentParser(description="TFTP Client")
    parser.add_argument("host", help="Server IP address", type=str)
    parser.add_argument("operation", help="get or put", choices=["get", "put"])
    parser.add_argument("filename", help="File to transfer", type=str)
    parser.add_argument("-p", "--port", help="Server port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()

    server_address = (args.host, args.port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)

    if args.operation == "get":
        send_rrq(sock, server_address, args.filename, DEFAULT_TRANSFER_MODE)
        receive_file(sock, args.filename)
    elif args.operation == "put":
        send_wrq(sock, server_address, args.filename, DEFAULT_TRANSFER_MODE)
        send_file(sock, args.filename)

    sock.close()


if __name__ == "__main__":
    main()
