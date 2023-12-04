#include <iostream>
#include <cstring>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

void client() {
    int s = socket(AF_INET, SOCK_STREAM, 0);
    if (s == -1) {
        std::cerr << "Error creating socket" << std::endl;
        return;
    }

    sockaddr_in serverAddress;
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_port = htons(57777);
    if (inet_pton(AF_INET, "0.0.0.0", &serverAddress.sin_addr) <= 0) {
        std::cerr << "Error converting IP address" << std::endl;
        close(s);
        return;
    }

    if (connect(s, (struct sockaddr*)&serverAddress, sizeof(serverAddress)) == -1) {
        std::cerr << "Error connecting to the server" << std::endl;
        close(s);
        return;
    }

    char buffer[1024];
    while (true) {
        ssize_t bytesReceived = recv(s, buffer, sizeof(buffer), 0);
        if (bytesReceived <= 0) {
            break;
        }
        buffer[bytesReceived] = '\0';
        std::cout << buffer << std::endl;

        std::string answer;
        std::cin >> answer;
        send(s, answer.c_str(), answer.size(), 0);
    }

    close(s);
}

int main() {
    client();
    return 0;
}