import socket
from akinator import (
    InvalidAnswer,
    Akinator,
    Answer,
    Theme,
)

# Definiți adresa și portul serverului
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 12345)
client_socket.bind(server_address)
print("Server is listening for incoming connections...")
data, client_address = client_socket.recvfrom(1024)  # 1024 is the buffer size
print(f"Received data from {client_address}: {data.decode('utf-8')}")

def test() -> None:
    # Creați o instanță Akinator
    aki = Akinator(
        child_mode=True,
        theme=Theme.from_str('characters'),
    )

    # Începe jocul și obține prima întrebare
    first_question = aki.start_game()
    # Primiți intrări de la consolă pentru prima întrebare
    message = f'{first_question}: '
    print(first_question)
    client_socket.sendto(message.encode('utf-8'), client_address)
    data = client_socket.recv(1024)
    answer = data.decode('utf-8')

    # Continuați să întrebați și să primiți răspunsuri atât timp cât progresul Akinatorului este <= 80
    while aki.progression <= 80:
        if answer == 'back':
            aki.back()
        else:
            try:
                # Parsați într-o variantă enumerată a răspunsului
                answer = Answer.from_str(answer)
            except InvalidAnswer:
                message = f'Invalid answer. type ok to repeat the question!\n'
                print(message)
            else:
                # Răspundeți la întrebarea curentă
                aki.answer(answer)

        # Primiți intrări de la consolă pentru următoarea întrebare
        message = f'{aki.question}: '
        client_socket.sendto(message.encode('utf-8'), client_address)
        data = client_socket.recv(1024)
        answer = data.decode('utf-8')

    # Spuneți Akinatorului să încheie jocul și să facă o presupunere
    first_guess = aki.win()

    if first_guess:
        # Afișați detaliile primei presupuneri
        message = f'name:' + first_guess.name
        client_socket.sendto(str(message).encode('utf-8'), client_address)


if __name__ == '__main__':
    test()
