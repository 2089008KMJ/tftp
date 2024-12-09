#!/usr/bin/python3
import socket
import struct
import os

TFTP_OPCODE_READ = 1
TFTP_OPCODE_WRITE = 2
TFTP_OPCODE_DATA = 3
TFTP_OPCODE_ACK = 4
TFTP_OPCODE_ERROR = 5

TFTP_PACKET_SIZE = 516
TFTP_DATA_BLOCK_SIZE = 512
TFTP_SOCKET_TIMEOUT = 5
TFTP_DEFAULT_PORT = 7540
TFTP_TRANSFER_MODE = "octet"

MESSAGE_TIMEOUT = "데이터 대기 중 타임아웃 발생."
MESSAGE_ACK_TIMEOUT = "ACK 응답 대기 중 타임아웃 발생."
MESSAGE_UNEXPECTED_RESPONSE = "예상치 못한 응답 또는 블록 번호 불일치."
MESSAGE_FILE_NOT_FOUND = "'{file_name}' 파일을 찾을 수 없습니다."


def build_tftp_request(opcode, file_name, transfer_mode=TFTP_TRANSFER_MODE):
    return struct.pack(f"!H{len(file_name) + 1}s{len(transfer_mode) + 1}s", opcode, file_name.encode(), transfer_mode.encode())


def build_tftp_ack(block_number):
    return struct.pack("!HH", TFTP_OPCODE_ACK, block_number)


def parse_tftp_data(packet):
    opcode, block_number = struct.unpack("!HH", packet[:4])
    data = packet[4:]
    return opcode, block_number, data


def tftp_upload_file(socket_instance, file_name, server_address):
    if not os.path.exists(file_name):
        print(MESSAGE_FILE_NOT_FOUND.format(file_name=file_name))
        return

    block_number = 0
    with open(file_name, 'rb') as file:
        while True:
            data_chunk = file.read(TFTP_DATA_BLOCK_SIZE)
            block_number += 1
            packet = struct.pack("!HH", TFTP_OPCODE_DATA, block_number) + data_chunk
            socket_instance.sendto(packet, server_address)

            try:
                response, _ = socket_instance.recvfrom(TFTP_PACKET_SIZE)
                opcode, ack_block = struct.unpack("!HH", response[:4])
                if opcode != TFTP_OPCODE_ACK or ack_block != block_number:
                    print(MESSAGE_UNEXPECTED_RESPONSE)
                    break
            except socket.timeout:
                print(MESSAGE_ACK_TIMEOUT)
                break

            if len(data_chunk) < TFTP_DATA_BLOCK_SIZE:
                print("업로드 완료.")
                break


def tftp_download_file(socket_instance, file_name, server_address):
    block_number = 0
    with open(file_name, 'wb') as file:
        while True:
            try:
                response, _ = socket_instance.recvfrom(TFTP_PACKET_SIZE)
                opcode, received_block, data_chunk = parse_tftp_data(response)

                if opcode != TFTP_OPCODE_DATA or received_block != block_number + 1:
                    print(MESSAGE_UNEXPECTED_RESPONSE)
                    break

                file.write(data_chunk)
                block_number = received_block
                ack_packet = build_tftp_ack(block_number)
                socket_instance.sendto(ack_packet, server_address)

                if len(data_chunk) < TFTP_DATA_BLOCK_SIZE:
                    print("다운로드 완료.")
                    break

            except socket.timeout:
                print(MESSAGE_TIMEOUT)
                break


def main():
    print("=== TFTP 클라이언트 ===")

    server_ip = input("TFTP 서버 IP를 입력하세요: ").strip()
    server_port = input(f"TFTP 서버 포트 번호를 입력하세요 : ").strip()
    server_port = int(server_port) if server_port else TFTP_DEFAULT_PORT

    operation_type = input("수행할 작업을 입력하세요 [get|put]: ").strip().lower()
    file_name = input("파일 이름을 입력하세요: ").strip()

    if not server_ip or not file_name or operation_type not in ['get', 'put']:
        print("잘못된 입력입니다. 올바른 IP, 작업, 파일 이름을 입력하세요.")
        return

    server_address = (server_ip, server_port)
    socket_instance = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_instance.settimeout(TFTP_SOCKET_TIMEOUT)

    try:
        if operation_type == "get":
            print(f"'{file_name}' 파일을 {server_ip}:{server_port}에서 다운로드 중...")
            request_packet = build_tftp_request(TFTP_OPCODE_READ, file_name)
            socket_instance.sendto(request_packet, server_address)
            tftp_download_file(socket_instance, file_name, server_address)

        elif operation_type == "put":
            print(f"'{file_name}' 파일을 {server_ip}:{server_port}로 업로드 중...")
            request_packet = build_tftp_request(TFTP_OPCODE_WRITE, file_name)
            socket_instance.sendto(request_packet, server_address)
            tftp_upload_file(socket_instance, file_name, server_address)

    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        socket_instance.close()
        print("연결을 종료합니다.")


if __name__ == "__main__":
    main()
