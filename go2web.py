from socket import *
import sys

search_engine = "Google"

def parse_args():
    # parse command line arguments
    if len(sys.argv) <= 1:
        print("Error: wrong format.")
        sys.exit(1)

    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        show_help()
        sys.exit(0)

    elif len(sys.argv) == 3 and sys.argv[1] == "-u":
        host = sys.argv[2]
        port = 80
        make_http_request(host, port)
        sys.exit(0)

    elif len(sys.argv) >= 3 and sys.argv[1] == "-s":
        print("Search command.")
        term = " ".join(sys.argv[2:])
        print("Search terms: " + term)
        sys.exit(0)

    else:
        print("Error: wrong format.")
        sys.exit(1)

def show_help():
    print("Usage: go2web [options]")
    print("Options:")
    print("  -h                Show this help message and exit")
    print("  -u <URL>         Make an HTTP request to the specified URL and print the response")
    print(f"  -s <search terms> Make an HTTP request to search the term using {search_engine} and print top 10 results")

def make_http_request(host, port):
    # Create a IPv4, TCP socket
    clientSocket = socket(AF_INET, SOCK_STREAM)

    # Establish a connection to the server
    clientSocket.connect((host, port))

    # Send an HTTP GET request to the server
    http_request = '''GET / HTTP/1.1\r\n
                Host: ''' + host + '''\r\n
                \r\n'''

    clientSocket.sendall(http_request.encode())

    # Receive the HTTP response from the server
    http_response_binary = b""
    while True:
        chunk = clientSocket.recv(4096)
        if not chunk:
            break
        http_response_binary += chunk

    http_response = http_response_binary.decode(errors="replace")

    parse_response(http_response)

    clientSocket.close()

def parse_response(http_response):
    # Extract response information
    header_end = http_response.find("\r\n\r\n")
    http_response_header = http_response[:header_end]

    status_line = http_response_header.splitlines()[0]
    protocol = status_line.split()[0]
    status_code = status_line.split()[1]
    status_message = " ".join(status_line.split()[2:])

    #   Split header before and after "Date: " and pick the part after
    #   Split the remaining string at the first occurrence of "\r\n" to get the date value
    date = http_response_header.split("Date: ")[1].split("\r\n")[0]

    expiration = http_response_header.split("Expires: ")[1].split("\r\n")[0]

    print("\tHTTP Response Header Information:")
    print(f"Protocol: {protocol}")
    print(f"Status Code: {status_code}")
    print(f"Status Message: {status_message}")
    print(f"Date: {date}")
    print(f"Expiration: {expiration}\n")

def main():
    parse_args()

    

if __name__ == "__main__":
    main()