# tftp
네트워크 프로그래밍 기말과제

# TFTP Client (TFTP 클라이언트)

## 📋 Description (설명)
A Python-based TFTP (Trivial File Transfer Protocol) client that supports both file download (`get`) and upload (`put`) operations. This client is designed to interact with a TFTP server, such as `tftpd-hpa`, following the standard TFTP protocol.  
(Python으로 구현된 TFTP(간단 파일 전송 프로토콜) 클라이언트입니다. 파일 다운로드(`get`)와 업로드(`put`) 기능을 모두 지원하며, `tftpd-hpa`와 같은 TFTP 서버와 상호작용할 수 있도록 설계되었습니다.)

## 💡 Features (주요 기능)
- Supports **file upload (WRQ)** and **file download (RRQ)**.  
  (**파일 업로드(WRQ)** 및 **파일 다운로드(RRQ)** 지원)
- Configurable server port (default: 69).  
  (기본 포트 69 이외에 사용자 정의 포트 설정 가능)
- Implements error handling for:  
  - File not found, access violations, illegal operations, etc.  
  - Timeout for both `ACK` and `DATA` responses.  
  (파일 없음, 접근 제한, 잘못된 요청 등 오류 처리와 `ACK` 및 `DATA` 응답 타임아웃 처리 지원)
- Transfers files in **octet (binary)** mode only.  
  (파일 전송 모드는 **octet(바이너리)**만 지원)

## ⚙️ Configuration (설정)
- **Host Address:** Server IP address.  
  (호스트 주소: 서버 IP 주소)
- **Transfer Mode:** Octet (binary) only.  
  (전송 모드: Octet(바이너리)만 지원)
- **Port:** Default is 69, can be customized using the `-p` flag.  
  (포트: 기본값은 69이며, `-p` 플래그로 변경 가능)
- **Timeout:** Default timeout is 5 seconds.  
  (타임아웃: 기본값은 5초)

## 📂 File Structure (파일 구조)
- **Main Script:** `Project2089008.py`  
  - Includes functions for `RRQ`, `WRQ`, `DATA`, `ACK`, and error handling.  
    (파일 다운로드(RRQ), 업로드(WRQ), 데이터 전송(DATA), 응답(ACK), 오류 처리를 포함한 주요 함수)

## 🚀 How to Run (실행 방법)
1. **Ensure a TFTP server (e.g., `tftpd-hpa`) is running.**  
   (TFTP 서버(`tftpd-hpa` 등)가 실행 중인지 확인)
2. **Execute the script from the terminal with appropriate arguments.**  
   (터미널에서 스크립트를 실행하고 적절한 인자를 입력)
3. **Verify file transfers in the working directory.**  
   (작업 디렉토리에서 파일 전송 결과 확인)

### Command-line Examples (명령행 실행 예시)
```bash
# Download a file from the server (서버에서 파일 다운로드)
python Project2089008.py 203.250.133.88 get test.txt

# Upload a file to the server (서버로 파일 업로드)
python Project2089008.py 203.250.133.88 put upload.txt

# Specify a custom port (사용자 정의 포트 사용)
python Project2089008.py 203.250.133.88 -p 9988 get config.txt

🛠 Requirements (필수 조건)
Python 3.x
A UDP-based TFTP server (e.g., tftpd-hpa)
(Python 3.x 및 UDP 기반 TFTP 서버)
📄 License (라이선스)
This project is open-source and available under the MIT License.
(이 프로젝트는 MIT 라이선스로 제공되며, 오픈 소스입니다.)
